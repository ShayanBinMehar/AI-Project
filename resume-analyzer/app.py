"""FastAPI backend for the Resume Analyzer."""

from __future__ import annotations

import io
from typing import Any

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from ai_feedback import generate_feedback
from history import get_analysis, list_analyses, save_analysis
from llm_client import get_llm_provider
from matcher import match_skills
from pdf_parser import extract_text_from_pdf
from skill_extractor import extract_skills

app = FastAPI(
    title="Resume Analyzer API",
    description="AI-powered resume vs job description analyzer",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    resume_text: str = Field(..., min_length=10)
    job_description: str = Field(..., min_length=10)
    save_history: bool = True
    resume_filename: str = ""


class AnalyzeResponse(BaseModel):
    match_score: float
    matched_skills: list[str]
    missing_skills: list[str]
    resume_skills: list[str]
    job_skills: list[str]
    strengths: str
    improvements: str
    suggested_learning: list[str]
    skill_extraction_method: str
    llm_provider: str
    analysis_id: str | None = None


def run_analysis(
    resume_text: str,
    job_description: str,
    save: bool = True,
    resume_filename: str = "",
) -> dict[str, Any]:
    """Core analysis pipeline shared by API and frontend."""
    resume_result = extract_skills(resume_text, source="resume")
    job_result = extract_skills(job_description, source="job description")

    resume_skills = resume_result["skills"]
    job_skills = job_result["skills"]

    match_result = match_skills(resume_skills, job_skills)
    feedback = generate_feedback(
        resume_text, job_description, resume_skills, job_skills, match_result
    )

    response: dict[str, Any] = {
        "match_score": match_result["match_score"],
        "matched_skills": match_result["matched_skills"],
        "missing_skills": match_result["missing_skills"],
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "strengths": feedback["strengths"],
        "improvements": feedback["improvements"],
        "suggested_learning": feedback["suggested_learning"],
        "skill_extraction_method": resume_result["method"],
        "llm_provider": get_llm_provider(),
    }

    if save:
        response["analysis_id"] = save_analysis(response, resume_filename)

    return response


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Resume Analyzer API",
        "docs": "/docs",
        "llm_provider": get_llm_provider(),
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "llm_provider": get_llm_provider()}


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)) -> dict[str, Any]:
    """Upload a PDF resume and extract clean text."""
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        text = extract_text_from_pdf(content)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Failed to parse PDF: {exc}") from exc

    if len(text.strip()) < 20:
        raise HTTPException(
            status_code=422,
            detail="Could not extract enough text from the PDF. Try a text-based PDF.",
        )

    return {
        "filename": file.filename,
        "text": text,
        "char_count": len(text),
    }


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> dict[str, Any]:
    """Analyze resume text against a job description."""
    return run_analysis(
        request.resume_text,
        request.job_description,
        save=request.save_history,
        resume_filename=request.resume_filename,
    )


@app.get("/history")
def history(limit: int = 20) -> dict[str, Any]:
    """List recent analysis history."""
    return {"analyses": list_analyses(limit=limit)}


@app.get("/history/{analysis_id}")
def history_detail(analysis_id: str) -> dict[str, Any]:
    """Get a single analysis from history."""
    record = get_analysis(analysis_id)
    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    return record


@app.get("/history/{analysis_id}/report")
def download_report(analysis_id: str) -> Any:
    """Download analysis as a text report."""
    from fastapi.responses import StreamingResponse

    record = get_analysis(analysis_id)
    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found.")

    report = _format_report(record)
    buffer = io.BytesIO(report.encode("utf-8"))
    return StreamingResponse(
        buffer,
        media_type="text/plain",
        headers={"Content-Disposition": f'attachment; filename="report-{analysis_id}.txt"'},
    )


def _format_report(record: dict[str, Any]) -> str:
    lines = [
        "RESUME ANALYSIS REPORT",
        "=" * 40,
        f"Analysis ID: {record.get('id', 'N/A')}",
        f"Date: {record.get('timestamp', 'N/A')}",
        f"Resume: {record.get('resume_filename', 'N/A')}",
        "",
        f"Match Score: {record.get('match_score', 0)}%",
        "",
        "Matched Skills:",
        ", ".join(record.get("matched_skills", [])) or "None",
        "",
        "Missing Skills:",
        ", ".join(record.get("missing_skills", [])) or "None",
        "",
        "Strengths:",
        record.get("strengths", ""),
        "",
        "Improvements:",
        record.get("improvements", ""),
        "",
        "Suggested Learning:",
        ", ".join(record.get("suggested_learning", [])) or "None",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
