from __future__ import annotations

import json
import os
from typing import Any

import streamlit as st
from openai import OpenAI

from src.config.settings import settings


class LLMProvider:
    def generate(self, prompt: str) -> str:
        raise NotImplementedError


class XKiroQwenProvider(LLMProvider):
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("XKIRO_API_KEY") or st.secrets.get("XKIRO_API_KEY", "") if hasattr(st, "secrets") else os.getenv("XKIRO_API_KEY")
        self.client = OpenAI(base_url=settings.openai_api_base, api_key=self.api_key or "")

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            raise ValueError("XKIRO API key is not configured.")
        response = self.client.chat.completions.create(
            model=settings.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        return response.choices[0].message.content or ""


@st.cache_resource
def get_llm() -> LLMProvider:
    """Return the configured LLM provider without exposing the concrete implementation."""
    return XKiroQwenProvider()


def safe_json_loads(payload: str) -> Any:
    """Parse JSON securely and tolerate code fences."""
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        cleaned = payload.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:].strip()
        return json.loads(cleaned)
