import os
import json
import logging
from typing import Any, Dict

# Import our core modules
# Note: In SageMaker, you might need to adjust python path or package structure
from src.ingest import IngestionEngine
from src.rag_engine import RAGEngine
from src.auditor import AuditorAgent
from src.config import settings
from langchain_community.chat_models import ChatBedrock

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Global variables to hold loaded models
rag_engine = None
auditor_agent = None

def model_fn(model_dir: str) -> Dict[str, Any]:
    """
    Load the model and resources for inference.
    This runs once when the container starts.
    """
    global rag_engine, auditor_agent
    
    logger.info("Loading models...")
    
    # 1. Initialize RAG Engine
    # In a real scenario, the vector store might be downloaded from S3 to model_dir
    vector_db_path = os.path.join(model_dir, settings.VECTOR_DB_PATH)
    
    # If not found in model_dir (local test), use config path
    if not os.path.exists(vector_db_path):
        vector_db_path = settings.VECTOR_DB_PATH

    rag_engine = RAGEngine(
        embedding_model_name=settings.EMBEDDING_MODEL_NAME,
        vector_store_path=vector_db_path
    )
    
    # 2. Initialize LLM (e.g., Bedrock)
    # Ensure AWS credentials are available via IAM Role
    llm = ChatBedrock(
        model_id=settings.LLM_MODEL_ID,
        model_kwargs={"temperature": 0.0}
    )
    
    # 3. Initialize Auditor
    auditor_agent = AuditorAgent(llm=llm, retriever=rag_engine.get_retriever())
    
    logger.info("Models loaded successfully.")
    return {"auditor": auditor_agent}

def input_fn(request_body: Any, request_content_type: str) -> Dict:
    """
    Parse the input request.
    """
    if request_content_type == 'application/json':
        return json.loads(request_body)
    else:
        raise ValueError(f"Unsupported content type: {request_content_type}")

def predict_fn(input_data: Dict, model: Dict) -> Dict:
    """
    Run the inference logic.
    """
    auditor = model['auditor']
    
    # Option A: Input is raw text or a query
    query = input_data.get("query", "Audit this project.")
    
    # Option B: Input is a document to ingest on the fly (slower, but possible)
    # if "document_text" in input_data: ...
    
    logger.info(f"Running audit for query: {query}")
    result = auditor.audit_project(query)
    
    return result.dict()

def output_fn(prediction: Dict, response_content_type: str) -> Any:
    """
    Format the output.
    """
    if response_content_type == 'application/json':
        return json.dumps(prediction)
    else:
        raise ValueError(f"Unsupported content type: {response_content_type}")

if __name__ == "__main__":
    # Local testing block
    print("Simulating SageMaker execution...")
    # Mock model_dir
    model = model_fn(".")
    result = predict_fn({"query": "Analyze the uploaded PUR."}, model)
    print(result)
