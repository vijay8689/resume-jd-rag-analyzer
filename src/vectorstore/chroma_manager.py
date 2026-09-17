from __future__ import annotations

from pathlib import Path

import chromadb
import streamlit as st
from chromadb.api.types import Metadata, Where

from src.config.settings import settings


class ChromaManager:
    def __init__(self) -> None:
        self.persist_directory = Path(settings.chroma_persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(self.persist_directory))
        self.collection = self.client.get_or_create_collection(name=settings.chroma_collection_name)

    def add_documents(self, documents: list[str], metadatas: list[Metadata], ids: list[str]) -> None:
        """Insert documents into the vector store."""
        self.collection.add(documents=documents, metadatas=metadatas, ids=ids)

    def query(self, query_text: str, where: dict | None = None, n_results: int = 5):
        """Run similarity search against the collection."""
        return self.collection.query(query_texts=[query_text], where=where, n_results=n_results)

    def delete_by_document(self, document_id: str, session_id: str | None = None) -> None:
        """Delete all Chroma records for the specified document."""
        where: Where = {"document_id": document_id}
        if session_id:
            where = {
                "$and": [
                    {"document_id": document_id},
                    {"session_id": session_id},
                ]
            }
        ids = self.collection.get(where=where, include=[]).get("ids", [])
        if ids:
            self.collection.delete(ids=ids)

    def reset_collection(self) -> None:
        """Delete and recreate the collection."""
        self.client.delete_collection(name=settings.chroma_collection_name)
        self.collection = self.client.get_or_create_collection(name=settings.chroma_collection_name)

    def count(self) -> int:
        return self.collection.count()


@st.cache_resource
def get_chroma_manager() -> ChromaManager:
    """Return a singleton-ish Chroma manager."""
    return ChromaManager()
