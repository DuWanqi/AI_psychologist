"""
Configuration file for the AI Psychologist application
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # API Configuration
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "YOUR_OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    
    # Memory Configuration
    DATA_STORAGE_PATH = os.getenv("DATA_STORAGE_PATH", "./data")
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./vector_db")
    
    # Model Configuration
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "openrouter/auto")
    
    # Memory Management
    WORKING_MEMORY_SIZE = int(os.getenv("WORKING_MEMORY_SIZE", "10"))
    EPISODIC_MEMORY_LIMIT = int(os.getenv("EPISODIC_MEMORY_LIMIT", "100"))
    
    # Procedural Memory Configuration
    THERAPEUTIC_TECHNIQUES_FILE = os.getenv("THERAPEUTIC_TECHNIQUES_FILE", "./config/therapeutic_techniques.json")
    
    # Application Settings
    APP_NAME = "AI Psychologist"
    VERSION = "0.1.0"