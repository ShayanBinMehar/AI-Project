"""Resume-to-job skill matching logic."""

from __future__ import annotations

import re


def _normalize(skill: str) -> str:
    return re.sub(r"\s+", " ", skill.strip().lower())


def _skill_matches(resume_skill: str, job_skill: str) -> bool:
    """Check if two skills match (exact or substring for variants)."""
    r = _normalize(resume_skill)
    j = _normalize(job_skill)
    if r == j:
        return True
    if len(r) >= 3 and len(j) >= 3:
        return r in j or j in r
    return False


def match_skills(resume_skills: list[str], job_skills: list[str]) -> dict:
    """
    Compare resume skills against job description skills.

    match_score = (matched_skills / total_job_skills) * 100
    """
    if not job_skills:
        return {
            "match_score": 100.0 if resume_skills else 0.0,
            "matched_skills": [],
            "missing_skills": [],
            "extra_skills": list(resume_skills),
        }

    matched: list[str] = []
    missing: list[str] = []

    for job_skill in job_skills:
        found = any(_skill_matches(r, job_skill) for r in resume_skills)
        if found:
            matched.append(job_skill)
        else:
            missing.append(job_skill)

    extra = [
        r for r in resume_skills
        if not any(_skill_matches(r, j) for j in job_skills)
    ]

    match_score = round((len(matched) / len(job_skills)) * 100, 1)

    return {
        "match_score": match_score,
        "matched_skills": matched,
        "missing_skills": missing,
        "extra_skills": extra,
    }
