import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Paths
    DATA_DIR: str = "data"
    VECTOR_DB_PATH: str = "vector_store_faiss"
    
    # Model Config
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    # Default to Amazon Titan (Serverless, no waitlist) to avoid "AccessDenied" on Claude
    LLM_MODEL_ID: str = "amazon.titan-text-express-v1" 
    
    # AWS Config (Optional if using local env vars or IAM roles)
    AWS_REGION: str = "us-east-1"
    
    # OpenAI (Optional, for local testing)
    OPENAI_API_KEY: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')

settings = Settings()

# Ensure directories exist
os.makedirs(settings.DATA_DIR, exist_ok=True)
