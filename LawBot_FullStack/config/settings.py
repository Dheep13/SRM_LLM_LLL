# Configuration Settings

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"

# Model configuration
MODEL_CONFIG = {
    "base_model": "Qwen/Qwen2.5-1.5B-Instruct",
    "adapter_path": str(MODELS_DIR / "adapters" / "lawbot_qwen_adapter"),  # Convert to string for compatibility
    "max_length": 2048,
    "temperature": 0.7,
    "top_p": 0.9,
}

# RAG configuration
RAG_CONFIG = {
    "embedding_model": "all-MiniLM-L6-v2",
    "vectorstore_path": str(DATA_DIR / "vectorstore" / "faiss_index"),  # Convert to string
    "chunks_path": str(DATA_DIR / "vectorstore" / "chunks.json"),
    "metadata_path": str(DATA_DIR / "vectorstore" / "metadata.json"),
    "top_k": 5,
    "similarity_threshold": 2.0,
}

# API configuration
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "debug": True,
    "cors_origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
}

# Legal tools configuration
LEGAL_TOOLS = {
    "dictionary": {
        "ipc": "Indian Penal Code - Criminal law of India",
        "crpc": "Code of Criminal Procedure - Procedure for criminal cases",
        "constitution": "Constitution of India - Supreme law of India",
        "bail": "Release of accused from custody pending trial",
        "arrest": "Taking of a person into custody for alleged offence",
        "murder": "Causing death with intention under IPC Section 300",
        "theft": "Taking movable property without consent under IPC Section 378",
    },
    "date_calculator": True,
    "case_lookup": True,
}

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
HF_TOKEN = os.getenv("HF_TOKEN", "")
INDIAN_KANOON_API_KEY = os.getenv("INDIAN_KANOON_API_KEY", "")
