from src.vectorstore.chroma_manager import ChromaManager


def test_session_isolation_metadata_filter():
    manager = ChromaManager()
    try:
        manager.collection.delete(where={})
    except Exception:
        pass
    manager.add_documents(["document text"], [{"session_id": "A", "document_id": "doc-a"}], ["id-a"])
    manager.add_documents(["document text b"], [{"session_id": "B", "document_id": "doc-b"}], ["id-b"])
    by_session = manager.collection.get(where={"session_id": "A"}, include=["documents"])
    assert "id-a" in by_session["ids"]
