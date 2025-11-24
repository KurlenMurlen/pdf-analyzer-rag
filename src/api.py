from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

# Load env vars explicitly
load_dotenv()

# Import our modules
from src.ingest import IngestionEngine
from src.rag_engine import RAGEngine
from src.auditor import AuditorAgent
from src.config import settings
from langchain_aws import ChatBedrock
from langchain_openai import ChatOpenAI
import boto3

app = FastAPI(title="R&D Auditor API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
class AppState:
    def __init__(self):
        self.rag_engine = None
        self.retriever = None
        self.llm = None
        self.auditor = None

state = AppState()

@app.on_event("startup")
async def startup_event():
    # Initialize RAG Engine
    state.rag_engine = RAGEngine(
        embedding_model_name=settings.EMBEDDING_MODEL_NAME,
        vector_store_path=settings.VECTOR_DB_PATH
    )
    
    # Initialize LLM
    try:
        print(f"Connecting to AWS Bedrock ({settings.AWS_REGION})...")
        bedrock_client = boto3.client(
            service_name="bedrock-runtime", 
            region_name=settings.AWS_REGION
        )
        state.llm = ChatBedrock(
            model_id=settings.LLM_MODEL_ID, 
            client=bedrock_client,
            model_kwargs={"temperature": 0.0}
        )
        print("✅ AWS Bedrock connected.")
    except Exception as e:
        print(f"⚠️ Bedrock connection failed: {e}. Trying OpenAI...")
        if settings.OPENAI_API_KEY:
            state.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
            print("✅ OpenAI connected.")
        else:
            print("❌ No LLM available.")

    # Load Vector Store if exists
    if os.path.exists(settings.VECTOR_DB_PATH):
        try:
            state.rag_engine.load_vector_store()
            state.retriever = state.rag_engine.get_retriever(k=10)
            if state.llm:
                state.auditor = AuditorAgent(llm=state.llm, retriever=state.retriever)
            print("✅ Vector store loaded.")
        except Exception as e:
            print(f"⚠️ Could not load vector store: {e}")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Ensure data directory exists
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        file_path = data_dir / file.filename
        
        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Process file
        ingestor = IngestionEngine(chunk_size=1000, chunk_overlap=200)
        documents = ingestor.process_file(str(file_path))
        
        if not documents:
            raise HTTPException(status_code=400, detail="No text extracted from PDF")
            
        # Update Vector Store
        state.rag_engine.create_vector_store(documents)
        state.rag_engine.load_vector_store()
        state.retriever = state.rag_engine.get_retriever(k=10)
        
        # Re-initialize auditor with new retriever
        if state.llm:
            state.auditor = AuditorAgent(llm=state.llm, retriever=state.retriever)
            
        return {"message": f"Successfully processed {file.filename}", "chunks": len(documents)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class AuditRequest(BaseModel):
    query: str = "Analise este projeto."
    system_prompt: str = "Você é um assistente de IA útil. Analise o documento fornecido e extraia as informações solicitadas em formato JSON."

import traceback

@app.post("/audit")
async def run_audit(request: AuditRequest):
    if not state.auditor:
        raise HTTPException(status_code=503, detail="Auditor not initialized (LLM or Vector Store missing)")
    
    try:
        print(f"Starting audit for query: {request.query}")
        # Pass both query and system_prompt to the auditor
        result = state.auditor.audit_project(request.query, request.system_prompt)
        
        # Result is now likely a dict or list, not a Pydantic model
        if isinstance(result, dict) or isinstance(result, list):
            return result
        
        # Fallback for legacy Pydantic objects if any remain
        if hasattr(result, 'model_dump'):
            return result.model_dump()
        if hasattr(result, 'dict'):
            return result.dict()
            
        return result
    except Exception as e:
        error_msg = f"Audit failed: {str(e)}"
        print(error_msg)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/health")
def health_check():
    return {"status": "ok", "llm": state.llm is not None, "vector_store": state.retriever is not None}
