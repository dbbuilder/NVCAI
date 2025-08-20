"""
Application configuration settings using Pydantic Settings
Handles environment variables and configuration management
"""
from typing import List, Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application Settings
    APP_NAME: str = "NVC AI Facilitator"
    APP_VERSION: str = "1.2.0-root-ui"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    
    # Database Configuration  
    DATABASE_URL: str = Field(default="sqlite:///./nvc_test.db", description="Database connection string")
    
    # AI Model API Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    
    # JWT Authentication
    JWT_SECRET_KEY: str = Field(default="test-jwt-secret-key-for-development-only-32-chars", min_length=32)
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Security Settings
    SECRET_KEY: str = Field(default="test-secret-key-for-development-only-32-characters", min_length=32)
    CORS_ORIGINS: List[str] = ["*"]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = None
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # WebSocket Configuration
    WS_HEARTBEAT_INTERVAL: int = 30
    
    # AI Model Settings
    DEFAULT_AI_MODEL: str = "openai"
    MAX_CONVERSATION_MEMORY: int = 10
    AI_RESPONSE_TIMEOUT: int = 30
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @validator("ALLOWED_HOSTS", pre=True)
    def assemble_allowed_hosts(cls, v):
        """Parse allowed hosts from string or list."""
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()