from typing import List, Optional
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
import os
import logging

logger = logging.getLogger(__name__)

class RAGEngine:
    def __init__(self, embedding_model_name: str, vector_store_path: str):
        self.embedding_model_name = embedding_model_name
        self.vector_store_path = vector_store_path
        self.embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model_name)
        self.vector_store: Optional[FAISS] = None

    def create_vector_store(self, documents: List[Document]) -> None:
        """
        Creates a new FAISS vector store from documents and saves it to disk.
        """
        if not documents:
            logger.warning("No documents to ingest.")
            return

        logger.info(f"Creating vector store with {len(documents)} chunks...")
        self.vector_store = FAISS.from_documents(documents, self.embeddings)
        self.vector_store.save_local(self.vector_store_path)
        logger.info(f"Vector store saved to {self.vector_store_path}")

    def load_vector_store(self) -> None:
        """
        Loads an existing FAISS vector store from disk.
        """
        if not os.path.exists(self.vector_store_path):
            raise FileNotFoundError(f"Vector store not found at {self.vector_store_path}")
            
        logger.info(f"Loading vector store from {self.vector_store_path}...")
        # allow_dangerous_deserialization is needed for local pickle files in newer versions
        self.vector_store = FAISS.load_local(
            self.vector_store_path, 
            self.embeddings, 
            allow_dangerous_deserialization=True
        )

    def get_retriever(self, k: int = 15, fetch_k: int = 50) -> VectorStoreRetriever:
        """
        Returns a retriever using Maximum Marginal Relevance (MMR).
        Increased k to ensure we capture enough context for a full audit.
        """
        if not self.vector_store:
            self.load_vector_store()
            
        return self.vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": k,
                "fetch_k": fetch_k,
                "lambda_mult": 0.7 # Increased slightly to favor relevance a bit more while keeping diversity
            }
        )
