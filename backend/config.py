from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path

from urllib.parse import quote_plus

class Settings(BaseSettings):
    youtube_api_key: Optional[str] = None
    tiktok_api_key: Optional[str] = None
    tiktok_rapidapi_host: str = "tiktok-scraper7.p.rapidapi.com"
    secret_key: str = "your-secret-key-keep-it-secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database settings
    db_user: str
    db_password: str
    db_host: str
    db_port: int = 3306
    db_name: str

    @property
    def database_url(self) -> str:
        encoded_password = quote_plus(self.db_password) if self.db_password else ""
        return f"mysql+pymysql://{self.db_user}:{encoded_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"

    @classmethod
    def get_api_key(cls) -> Optional[str]:
        """Get YouTube API key from environment"""
        settings = cls()
        return settings.youtube_api_key

    @classmethod
    def get_tiktok_api_key(cls) -> Optional[str]:
        """Get TikTok API key from environment"""
        settings = cls()
        return settings.tiktok_api_key
    
    @classmethod
    def save_api_key(cls, api_key: str) -> bool:
        """Save API key to .env file"""
        try:
            env_path = Path(".env")
            
            # Read existing content
            existing_content = {}
            if env_path.exists():
                with open(env_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            existing_content[key] = value
            
            # Update API key
            existing_content['YOUTUBE_API_KEY'] = api_key
            
            # Write back
            with open(env_path, 'w') as f:
                for key, value in existing_content.items():
                    f.write(f"{key}={value}\n")
            
            return True
        except Exception as e:
            print(f"Error saving API key: {e}")
            return False
    
    @classmethod
    def delete_api_key(cls) -> bool:
        """Remove API key from .env file"""
        try:
            env_path = Path(".env")
            if not env_path.exists():
                return True
            
            # Read and filter content
            lines = []
            with open(env_path, 'r') as f:
                for line in f:
                    if not line.strip().startswith('YOUTUBE_API_KEY='):
                        lines.append(line)
            
            # Write back
            with open(env_path, 'w') as f:
                f.writelines(lines)
            
            return True
        except Exception as e:
            print(f"Error deleting API key: {e}")
            return False
    
    @classmethod
    def save_tiktok_api_key(cls, api_key: str) -> bool:
        """Save TikTok API key to .env file"""
        try:
            env_path = Path(".env")
            
            # Read existing content
            existing_content = {}
            if env_path.exists():
                with open(env_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            existing_content[key] = value
            
            # Update TikTok API key
            existing_content['TIKTOK_API_KEY'] = api_key
            
            # Write back
            with open(env_path, 'w') as f:
                for key, value in existing_content.items():
                    f.write(f"{key}={value}\n")
            
            return True
        except Exception as e:
            print(f"Error saving TikTok API key: {e}")
            return False
    
    @classmethod
    def delete_tiktok_api_key(cls) -> bool:
        """Remove TikTok API key from .env file"""
        try:
            env_path = Path(".env")
            if not env_path.exists():
                return True
            
            # Read and filter content
            lines = []
            with open(env_path, 'r') as f:
                for line in f:
                    if not line.strip().startswith('TIKTOK_API_KEY='):
                        lines.append(line)
            
            # Write back
            with open(env_path, 'w') as f:
                f.writelines(lines)
            
            return True
        except Exception as e:
            print(f"Error deleting TikTok API key: {e}")
            return False

settings = Settings()
