from __future__ import annotations

import streamlit as st
from sentence_transformers import SentenceTransformer

from src.config.settings import settings


@st.cache_resource
def get_embedding_model():
    """Load the local embedding model once and cache it."""
    return SentenceTransformer(settings.embedding_model)


def embed_texts(texts: list[str]):
    """Encode a list of strings into embeddings."""
    model = get_embedding_model()
    return model.encode(texts, convert_to_numpy=True)
