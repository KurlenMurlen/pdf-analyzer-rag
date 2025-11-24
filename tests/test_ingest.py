import pytest
from src.ingest import PDFLoader

def test_pdf_loader_valid_file():
    loader = PDFLoader("path/to/valid_file.pdf")
    content = loader.load()
    assert content is not None
    assert isinstance(content, str)
    assert len(content) > 0

def test_pdf_loader_invalid_file():
    loader = PDFLoader("path/to/invalid_file.pdf")
    with pytest.raises(FileNotFoundError):
        loader.load()

def test_semantic_chunking():
    loader = PDFLoader("path/to/valid_file.pdf")
    content = loader.load()
    chunks = loader.semantic_chunk(content)
    assert len(chunks) > 0
    assert all(isinstance(chunk, str) for chunk in chunks)
    # Add more specific assertions based on expected chunk content

def test_chunking_for_technical_sections():
    loader = PDFLoader("path/to/valid_file.pdf")
    content = loader.load()
    chunks = loader.semantic_chunk(content)
    # Assuming we expect certain sections to be present
    assert any("Metodologia" in chunk for chunk in chunks)
    assert any("Objetivos" in chunk for chunk in chunks)