from src.chunking.chunker import chunk_text


def test_chunk_text_produces_segments():
    text = "Section one.\n\nSection two.\n\nSection three."
    chunks = chunk_text(text, "General")
    assert len(chunks) >= 2
    assert all(isinstance(chunk, str) for chunk in chunks)
