from types import SimpleNamespace

from src.vectorstore import chroma_manager


def test_embedding_cache_uses_project_storage_from_other_working_directory(tmp_path, monkeypatch):
    project = tmp_path / "project"
    monkeypatch.setattr(chroma_manager, "__file__", str(project / "src/vectorstore/chroma_manager.py"))
    monkeypatch.setattr(chroma_manager.settings, "chroma_model_cache_directory", "data/model_cache/chroma")
    monkeypatch.setattr(chroma_manager.settings, "chroma_persist_directory", str(tmp_path / "db"))
    # Restore the process-wide model path after this test.
    monkeypatch.setattr(chroma_manager.ONNXMiniLM_L6_V2, "DOWNLOAD_PATH", tmp_path / "protected_home")
    monkeypatch.chdir(tmp_path)
    client = SimpleNamespace(get_or_create_collection=lambda **kwargs: object())
    monkeypatch.setattr(chroma_manager.chromadb, "PersistentClient", lambda **kwargs: client)

    chroma_manager.ChromaManager()

    cache = chroma_manager.ONNXMiniLM_L6_V2.DOWNLOAD_PATH
    assert cache == project / "data/model_cache/chroma/all-MiniLM-L6-v2"
    assert cache.is_dir()
    assert not (tmp_path / "protected_home").exists()
