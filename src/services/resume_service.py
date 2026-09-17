from __future__ import annotations

import re
import uuid
from pathlib import Path
from tempfile import TemporaryDirectory

from chromadb.api.types import Where

from src.chunking.chunker import chunk_text
from src.config.settings import settings
from src.ingestion.document_processor import clean_text, detect_sections, extract_text_from_file
from src.vectorstore.chroma_manager import get_chroma_manager


class ResumeService:
    def process_uploaded_resume(self, uploaded_file, session_id: str) -> dict:
        """Validate, extract, chunk and index the uploaded resume."""
        file_bytes = uploaded_file.read()
        if len(file_bytes) > settings.max_upload_size_kb * 1024:
            raise ValueError(f"File exceeds {settings.max_upload_size_kb} KB upload limit.")

        safe_name = re.sub(r"[^A-Za-z0-9_.-]", "_", uploaded_file.name or "resume")
        document_id = uuid.uuid4().hex
        suffix = Path(safe_name).suffix.lower().replace('.', '')

        with TemporaryDirectory() as tmp_dir:
            temp_path = Path(tmp_dir) / safe_name
            temp_path.write_bytes(file_bytes)

            file_kind = self._detect_file_type(suffix)
            raw_text = extract_text_from_file(file_kind, temp_path)
            cleaned = clean_text(raw_text)
            sections = detect_sections(cleaned)
            section_name = sections[0].get("section", "General") if sections else "General"
            chunked = chunk_text(cleaned, section_name)

            manager = get_chroma_manager()
            metadata_list = []
            for index, chunk in enumerate(chunked):
                metadata_list.append(
                    {
                        "chunk_id": f"chunk_{index:03d}",
                        "document_id": document_id,
                        "session_id": session_id,
                        "source": safe_name,
                        "section": "General",
                        "page": 1,
                        "text": chunk,
                    }
                )

            manager.add_documents(
                documents=chunked,
                metadatas=metadata_list,
                ids=[f"{document_id}_{index:03d}" for index in range(len(chunked))],
            )

        return {
            "document_id": document_id,
            "filename": safe_name,
            "chunk_count": len(chunked),
            "section_count": len(sections or [{"section": "General"}]),
            "characters": len(cleaned),
            "status": "indexed",
        }

    def clear_session_data(self, session_id: str) -> None:
        """Remove all indexed documents for a session."""
        manager = get_chroma_manager()
        where: Where = {"session_id": session_id}
        ids = manager.collection.get(where=where, include=[]).get("ids", [])
        if ids:
            manager.collection.delete(ids=ids)

    @staticmethod
    def _detect_file_type(extension: str) -> str:
        mapping = {"pdf": "pdf", "docx": "docx", "txt": "txt"}
        if extension not in mapping:
            raise ValueError("Unsupported file type")
        return mapping[extension]
