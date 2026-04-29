"""Configuration management for the YouTube Analysis Agent System"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for the application"""
    
    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    
    # Ollama Configuration
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "mistral")
    OLLAMA_TIMEOUT: int = 120  # seconds
    
    # Memory Configuration
    MEMORY_TYPE: str = os.getenv("MEMORY_TYPE", "chromadb")
    MEMORY_PATH: str = os.getenv("MEMORY_PATH", str(DATA_DIR / "memory"))
    
    # Transcript Cache
    TRANSCRIPT_CACHE: str = os.getenv("TRANSCRIPT_CACHE", str(DATA_DIR / "transcripts"))
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    
    # Model Parameters
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2000"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    TOP_P: float = float(os.getenv("TOP_P", "0.95"))
    
    # System Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    def __init__(self):
        """Initialize configuration and create necessary directories"""
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories if they don't exist"""
        Path(self.MEMORY_PATH).mkdir(parents=True, exist_ok=True)
        Path(self.TRANSCRIPT_CACHE).mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def validate_ollama_connection() -> bool:
        """Validate connection to Ollama server"""
        import requests
        try:
            response = requests.get(
                f"{Config.OLLAMA_BASE_URL}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error connecting to Ollama: {e}")
            return False
    
    def to_dict(self) -> dict:
        """Convert config to dictionary"""
        return {
            k: v for k, v in self.__dict__.items()
            if not k.startswith("_")
        }


# Global config instance
config = Config()
