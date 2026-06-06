"""Streamlit frontend for the Resume Analyzer."""

from __future__ import annotations

from dotenv import load_dotenv
import streamlit as st

load_dotenv()

from app import run_analysis
from history import list_analyses
from llm_client import get_llm_provider
from pdf_parser import extract_text_from_pdf

st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide",
)

st.title("📄 AI Resume Analyzer")
st.caption("Upload a resume, paste a job description, and get AI-powered match insights.")

provider = get_llm_provider()
provider_labels = {
    "gemini": "🟢 Google Gemini",
    "none": "🔴 Keyword fallback (set GEMINI_API_KEY)",
}
st.info(f"LLM Provider: {provider_labels.get(provider, provider)}")

tab_analyze, tab_history = st.tabs(["Analyze", "History"])

with tab_analyze:
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Resume")
        uploaded = st.file_uploader("Upload PDF resume", type=["pdf"])
        resume_text = st.text_area(
            "Or paste resume text",
            height=300,
            placeholder="Resume text will appear here after upload, or paste manually...",
        )

        if uploaded:
            text = extract_text_from_pdf(uploaded.read())
            st.session_state["resume_text"] = text
            st.session_state["resume_filename"] = uploaded.name
            resume_text = text
            st.success(f"Extracted {len(text):,} characters from **{uploaded.name}**")

    with col_right:
        st.subheader("Job Description")
        job_description = st.text_area(
            "Paste the job description",
            height=400,
            placeholder="Paste the full job description here...",
        )

    analyze_btn = st.button("🔍 Analyze Match", type="primary", use_container_width=True)

    if analyze_btn:
        final_resume = st.session_state.get("resume_text", resume_text)
        if not final_resume or len(final_resume.strip()) < 20:
            st.error("Please upload a PDF or paste resume text (at least 20 characters).")
        elif not job_description or len(job_description.strip()) < 20:
            st.error("Please paste a job description (at least 20 characters).")
        else:
            with st.spinner("Analyzing resume against job description..."):
                try:
                    result = run_analysis(
                        final_resume,
                        job_description,
                        save=True,
                        resume_filename=st.session_state.get("resume_filename", ""),
                    )
                    st.session_state["last_result"] = result
                except Exception as exc:
                    st.error(f"Analysis failed: {exc}")

    if "last_result" in st.session_state:
        result = st.session_state["last_result"]
        st.divider()
        st.subheader("Results")

        score = result["match_score"]
        if score >= 75:
            st.success(f"Match Score: **{score}%** — Strong match")
        elif score >= 50:
            st.warning(f"Match Score: **{score}%** — Moderate match")
        else:
            st.error(f"Match Score: **{score}%** — Needs improvement")

        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Matched Skills", len(result["matched_skills"]))
        with m2:
            st.metric("Missing Skills", len(result["missing_skills"]))
        with m3:
            st.metric("Resume Skills", len(result["resume_skills"]))

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**✅ Matched Skills**")
            if result["matched_skills"]:
                st.write(", ".join(result["matched_skills"]))
            else:
                st.write("None")

            st.markdown("**💪 Strengths**")
            st.write(result["strengths"])

        with c2:
            st.markdown("**❌ Missing Skills**")
            if result["missing_skills"]:
                for skill in result["missing_skills"]:
                    st.markdown(f"- :red[{skill}]")
            else:
                st.write("None — great coverage!")

            st.markdown("**📈 How to Improve**")
            st.write(result["improvements"])

        st.markdown("**📚 Suggested Learning**")
        st.write(", ".join(result["suggested_learning"]) or "None")

        with st.expander("Full JSON Response"):
            st.json(result)

        if result.get("analysis_id"):
            st.caption(f"Saved to history — ID: `{result['analysis_id']}`")

with tab_history:
    st.subheader("Analysis History")
    records = list_analyses(limit=30)

    if not records:
        st.info("No analyses yet. Run your first analysis in the Analyze tab.")
    else:
        for record in records:
            with st.expander(
                f"{record.get('resume_filename') or 'Untitled'} — "
                f"{record.get('match_score', 0)}% — "
                f"{record.get('timestamp', '')[:19]}"
            ):
                st.write(f"**ID:** {record.get('id')}")
                st.write(f"**Matched:** {', '.join(record.get('matched_skills', []))}")
                st.write(f"**Missing:** {', '.join(record.get('missing_skills', []))}")
                st.write(f"**Strengths:** {record.get('strengths', '')}")
                st.json(record)
