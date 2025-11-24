import pdfplumber
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IngestionEngine:
    """
    Engine responsible for ingesting PDF documents and chunking them 
    for RAG processing.
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
            length_function=len,
        )

    def load_pdf(self, file_path: str) -> List[Document]:
        """
        Loads a PDF file and returns a list of LangChain Documents,
        one per page, with metadata.
        """
        documents = []
        try:
            with pdfplumber.open(file_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        # Clean up some common PDF artifacts if necessary
                        text = text.strip()
                        
                        metadata = {
                            "source": file_path,
                            "page": i + 1,
                            "total_pages": len(pdf.pages)
                        }
                        documents.append(Document(page_content=text, metadata=metadata))
            
            logger.info(f"Successfully loaded {len(documents)} pages from {file_path}")
            return documents
        except Exception as e:
            logger.error(f"Error loading PDF {file_path}: {e}")
            raise

    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Splits documents into smaller semantic chunks.
        """
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Split {len(documents)} pages into {len(chunks)} chunks.")
        return chunks

    def process_file(self, file_path: str) -> List[Document]:
        """
        End-to-end processing: Load -> Chunk.
        """
        raw_docs = self.load_pdf(file_path)
        return self.chunk_documents(raw_docs)