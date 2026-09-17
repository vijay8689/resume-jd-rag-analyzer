import os
from dataclasses import dataclass


@dataclass
class Settings:
    model_name: str = os.getenv("MODEL_NAME", "qwen/qwen3.7-flash:free")
    openai_api_base: str = os.getenv("OPENAI_API_BASE", "https://api.xkiro.com/v1")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    chroma_persist_directory: str = os.getenv("CHROMA_PERSIST_DIRECTORY", "./data/chroma")
    chroma_collection_name: str = os.getenv("CHROMA_COLLECTION_NAME", "resume_documents")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "700"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "100"))
    top_k: int = int(os.getenv("TOP_K", "5"))
    match_threshold: float = float(os.getenv("MATCH_THRESHOLD", "0.70"))
    partial_threshold: float = float(os.getenv("PARTIAL_THRESHOLD", "0.50"))
    max_upload_size_kb: int = int(os.getenv("MAX_UPLOAD_SIZE_KB", "500"))
    llm_enabled: bool = os.getenv("LLM_ENABLED", "true").lower() == "true"


settings = Settings()
