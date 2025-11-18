import os
from typing import Optional

# 尝试导入 dotenv，如果不可用则提供空实现
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    def load_dotenv():
        pass
    # 如果 dotenv 不可用，尝试从环境变量加载
    pass

class Config:
    """Configuration class for the AI Psychologist"""
    
    # API 配置
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    
    # 模型配置
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "openrouter/auto")
    
    # Ollama 配置
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2:latest")
    
    # 模型选择配置
    MODEL_PROVIDER: str = os.getenv("MODEL_PROVIDER", "openrouter")  # "openrouter" 或 "ollama"
    
    # 存储路径
    DATA_STORAGE_PATH: str = os.getenv("DATA_STORAGE_PATH", "./data")
    VECTOR_DB_PATH: str = os.getenv("VECTOR_DB_PATH", "./vector_db")
    
    # 内存配置
    WORKING_MEMORY_SIZE: int = int(os.getenv("WORKING_MEMORY_SIZE", "10"))
    EPISODIC_MEMORY_LIMIT: int = int(os.getenv("EPISODIC_MEMORY_LIMIT", "100"))
    
    # 程序性记忆配置
    THERAPEUTIC_TECHNIQUES_FILE: str = os.getenv(
        "THERAPEUTIC_TECHNIQUES_FILE", 
        "./config/therapeutic_techniques.json"
    )