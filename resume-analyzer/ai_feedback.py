"""AI-powered feedback for resume improvement."""

from __future__ import annotations

from typing import Any

from llm_client import chat_completion_json, get_llm_provider


def _fallback_feedback(
    match_result: dict,
    resume_skills: list[str],
    job_skills: list[str],
) -> dict[str, Any]:
    """Generate basic feedback without an LLM."""
    matched = match_result["matched_skills"]
    missing = match_result["missing_skills"]
    extra = match_result.get("extra_skills", [])

    strengths_parts = []
    if matched:
        strengths_parts.append(
            f"Strong alignment in: {', '.join(matched[:5])}"
        )
    if extra:
        strengths_parts.append(
            f"Additional skills beyond requirements: {', '.join(extra[:5])}"
        )

    strengths = (
        ". ".join(strengths_parts)
        if strengths_parts
        else "Review resume to highlight relevant experience more clearly."
    )

    improvements = (
        f"Emphasize experience with {', '.join(missing[:5])} in your resume. "
        "Add specific projects, metrics, and tools used for each missing skill."
        if missing
        else "Your resume covers the key requirements. Consider adding quantifiable achievements."
    )

    return {
        "strengths": strengths,
        "improvements": improvements,
        "suggested_learning": missing[:5],
    }


def generate_feedback(
    resume_text: str,
    job_description: str,
    resume_skills: list[str],
    job_skills: list[str],
    match_result: dict,
) -> dict[str, Any]:
    """Generate intelligent resume feedback using LLM or fallback logic."""
    if get_llm_provider() == "none":
        return _fallback_feedback(match_result, resume_skills, job_skills)

    prompt = f"""Analyze this resume against the job description and provide actionable feedback.

Return JSON in this exact format:
{{
  "strengths": "2-3 sentences on what the candidate is strong at",
  "improvements": "2-3 sentences on how to improve the resume",
  "suggested_learning": ["skill1", "skill2"]
}}

Resume skills: {resume_skills}
Job required skills: {job_skills}
Matched skills: {match_result['matched_skills']}
Missing skills: {match_result['missing_skills']}
Match score: {match_result['match_score']}%

Resume excerpt:
{resume_text[:3000]}

Job description:
{job_description[:3000]}
"""
    try:
        result = chat_completion_json(
            prompt,
            system="You are an expert career coach and technical recruiter.",
        )
        return {
            "strengths": result.get("strengths", ""),
            "improvements": result.get("improvements", ""),
            "suggested_learning": result.get("suggested_learning", match_result["missing_skills"]),
        }
    except Exception:
        return _fallback_feedback(match_result, resume_skills, job_skills)
