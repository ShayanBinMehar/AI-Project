"""Shared LLM client using Google Gemini API."""

from __future__ import annotations

import json
import os
import re
from typing import Any

from google import genai
from google.genai import types

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")


def get_llm_provider() -> str:
    """Return active provider: gemini or none."""
    return "gemini" if GEMINI_API_KEY else "none"


def _get_client() -> genai.Client:
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "Gemini API key not set. Add GEMINI_API_KEY to your .env file."
        )
    return genai.Client(api_key=GEMINI_API_KEY)


def _extract_json(text: str) -> dict[str, Any]:
    """Parse JSON from LLM response, tolerating markdown fences."""
    text = text.strip()
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if fence_match:
        text = fence_match.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        brace_match = re.search(r"\{[\s\S]*\}", text)
        if brace_match:
            return json.loads(brace_match.group())
        raise


def chat_completion(prompt: str, system: str = "") -> str:
    """Send a chat completion request to Gemini."""
    client = _get_client()
    config_kwargs: dict[str, Any] = {"temperature": 0.2}
    if system:
        config_kwargs["system_instruction"] = system

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(**config_kwargs),
    )
    return response.text or ""


def chat_completion_json(prompt: str, system: str = "") -> dict[str, Any]:
    """Request structured JSON output from Gemini."""
    json_system = (
        f"{system}\n\nRespond with valid JSON only. No markdown or extra text."
        if system
        else "Respond with valid JSON only. No markdown or extra text."
    )
    raw = chat_completion(prompt, json_system)
    return _extract_json(raw)
