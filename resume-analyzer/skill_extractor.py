"""Skill extraction from resume and job description text."""

from __future__ import annotations

import re
from typing import Any

from llm_client import chat_completion_json, get_llm_provider

# Common technical and professional skills for keyword fallback
SKILL_KEYWORDS = [
    "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust", "Ruby",
    "PHP", "Swift", "Kotlin", "Scala", "R", "MATLAB", "SQL", "NoSQL", "HTML", "CSS",
    "React", "Angular", "Vue", "Node.js", "Django", "Flask", "FastAPI", "Spring",
    "Express", "Next.js", "REST API", "GraphQL", "Machine Learning", "Deep Learning",
    "NLP", "Computer Vision", "Data Analysis", "Data Science", "Statistics",
    "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy", "Spark", "Hadoop",
    "AWS", "Azure", "GCP", "Docker", "Kubernetes", "CI/CD", "Jenkins", "Git",
    "Linux", "Agile", "Scrum", "Project Management", "Communication", "Leadership",
    "Problem Solving", "Tableau", "Power BI", "Excel", "MongoDB", "PostgreSQL",
    "MySQL", "Redis", "Elasticsearch", "Kafka", "Microservices", "DevOps",
    "Terraform", "Ansible", "Cloud Computing", "Cybersecurity", "Testing",
    "Unit Testing", "Selenium", "JIRA", "Figma", "UI/UX", "Blockchain",
    "Solidity", "Android", "iOS", "Flutter", "React Native", "SAP", "Salesforce",
    "ETL", "Airflow", "dbt", "Snowflake", "BigQuery", "Redshift", "LLM",
    "OpenAI", "LangChain", "Vector Database", "Prompt Engineering",
]


def _normalize_skill(skill: str) -> str:
    return re.sub(r"\s+", " ", skill.strip())


def _dedupe_skills(skills: list[str]) -> list[str]:
    seen: dict[str, str] = {}
    for skill in skills:
        normalized = _normalize_skill(skill)
        if not normalized:
            continue
        key = normalized.lower()
        if key not in seen:
            seen[key] = normalized
    return list(seen.values())


def extract_skills_keyword(text: str) -> list[str]:
    """Extract skills using keyword matching (fallback)."""
    text_lower = text.lower()
    found: list[str] = []

    for skill in SKILL_KEYWORDS:
        pattern = re.escape(skill.lower())
        if re.search(rf"\b{pattern}\b", text_lower):
            found.append(skill)

    return _dedupe_skills(found)


def extract_skills_llm(text: str, source: str = "document") -> list[str]:
    """Extract skills using an LLM, returning structured JSON."""
    prompt = f"""Extract all technical and professional skills from this {source}.

Return JSON in this exact format:
{{"skills": ["Skill1", "Skill2"]}}

Rules:
- Include programming languages, frameworks, tools, cloud platforms, methodologies
- Include soft skills only if clearly emphasized
- Use standard capitalization (e.g., "Python", "Machine Learning")
- Do not invent skills not present in the text

Text:
{text[:8000]}
"""
    result = chat_completion_json(
        prompt,
        system="You are an expert resume and job description analyst.",
    )
    skills = result.get("skills", [])
    if not isinstance(skills, list):
        return []
    return _dedupe_skills([str(s) for s in skills])


def extract_skills(text: str, source: str = "document") -> dict[str, Any]:
    """Extract skills, preferring LLM with keyword fallback."""
    method = "keyword"
    skills: list[str] = []

    if get_llm_provider() != "none":
        try:
            skills = extract_skills_llm(text, source)
            method = "llm"
        except Exception:
            skills = extract_skills_keyword(text)
            method = "keyword_fallback"
    else:
        skills = extract_skills_keyword(text)

    return {"skills": skills, "method": method}
