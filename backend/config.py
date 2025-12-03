from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    youtube_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

    @classmethod
    def get_api_key(cls) -> Optional[str]:
        """Get YouTube API key from environment"""
        settings = cls()
        return settings.youtube_api_key
    
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

settings = Settings()
