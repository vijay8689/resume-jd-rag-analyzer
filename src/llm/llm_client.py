from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import streamlit as st
from openai import OpenAI
from dotenv import dotenv_values
from streamlit.errors import StreamlitSecretNotFoundError

from src.config.settings import settings


class MissingAPIKeyError(ValueError):
    """The optional language model has not been configured."""


def resolve_api_key(api_key: str | None = None) -> str:
    """Read credentials without requiring a Streamlit secrets file."""
    value = api_key or os.getenv("XKIRO_API_KEY")
    if not value:
        env_path = Path(__file__).resolve().parents[2] / ".env"
        value = dotenv_values(env_path).get("XKIRO_API_KEY")
    if not value:
        try:
            value = st.secrets.get("XKIRO_API_KEY", "")
        except StreamlitSecretNotFoundError:
            value = ""
    value = (value or "").strip()
    if not value or value == "replace-with-your-xkiro-api-key":
        raise MissingAPIKeyError(
            "Interview preparation requires an XKIRO API key. Set XKIRO_API_KEY "
            "in the project's .env file, your environment, or .streamlit/secrets.toml."
        )
    return value


class LLMProvider:
    def generate(self, prompt: str) -> str:
        raise NotImplementedError


class XKiroQwenProvider(LLMProvider):
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = resolve_api_key(api_key)
        self.client = OpenAI(base_url=settings.openai_api_base, api_key=self.api_key)

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
