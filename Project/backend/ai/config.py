"""
Configuration Management for AI Engine
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # App Info
    APP_NAME: str = "SmartOps AI - RCA Engine"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8002
    
    # Google Gemini
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-flash-latest"  # or gemini-pro-latest for better quality
    
    # Database
    DATABASE_URL: str = "sqlite:///./smartops_ai.db"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001,http://localhost:5173,http://localhost:5174,http://localhost:5175,http://localhost:5176"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS_ORIGINS string to list"""
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        return self.CORS_ORIGINS
    
    # External Services
    INVESTIGATION_BACKEND_URL: str = "http://localhost:8000"
    CHAOS_PLATFORM_URL: str = "http://localhost:8001"
    
    # AI Parameters
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 2048
    
    # RAG Settings
    SIMILARITY_THRESHOLD: float = 0.75
    MAX_SIMILAR_INCIDENTS: int = 3
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
