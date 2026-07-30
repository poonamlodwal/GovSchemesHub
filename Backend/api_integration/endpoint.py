import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv())


@dataclass
class SchemHubConfig:
    """Configuration for SchemHub API client"""
    
    # API Base Configuration
    base_url: str = os.getenv("SCHEMEHUB_BASE_URL", "https://schemeshub.netlify.app")
    
    # Authentication Configuration
    auth_type: str = os.getenv("SCHEMEHUB_AUTH_TYPE", "api_key").lower()
    api_key: Optional[str] = os.getenv("GOV_API_KEY")
    username: Optional[str] = os.getenv("SCHEMEHUB_USERNAME")
    password: Optional[str] = os.getenv("SCHEMEHUB_PASSWORD")
    bearer_token: Optional[str] = os.getenv("SCHEMEHUB_BEARER_TOKEN")
    
    # Request Configuration
    timeout: int = int(os.getenv("SCHEMEHUB_TIMEOUT", "30"))
    verify_ssl: bool = os.getenv("SCHEMEHUB_VERIFY_SSL", "true").lower() == "true"
    
    # Retry Configuration
    max_retries: int = int(os.getenv("SCHEMEHUB_MAX_RETRIES", "3"))
    retry_backoff_factor: float = float(os.getenv("SCHEMEHUB_RETRY_BACKOFF", "0.5"))
    
    # Logging Configuration
    log_level: str = os.getenv("SCHEMEHUB_LOG_LEVEL", "INFO")
    
    def validate(self) -> bool:
        """
        Validate the configuration.
        
        Returns:
            True if valid, raises ValueError otherwise
        """
        if not self.base_url:
            raise ValueError("SCHEMEHUB_BASE_URL is required")
        
        if self.auth_type not in ["api_key", "bearer", "basic"]:
            raise ValueError(f"Invalid auth_type: {self.auth_type}")
        
        if self.auth_type == "api_key" and not self.api_key:
           raise ValueError("GOV_API_KEY is required for 'api_key' authentication")        
        if self.auth_type == "bearer" and not self.bearer_token:
            raise ValueError("SCHEMEHUB_BEARER_TOKEN is required for 'bearer' authentication")
        
        if self.auth_type == "basic" and (not self.username or not self.password):
            raise ValueError("SCHEMEHUB_USERNAME and SCHEMEHUB_PASSWORD are required for 'basic' authentication")
        
        return True

    @classmethod
    def from_env(cls) -> "SchemHubConfig":
        """
        Create configuration from environment variables.
        
        Returns:
            SchemHubConfig instance
        """
        config = cls()
        config.validate()
        return config
