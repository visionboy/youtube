from config import Settings
from typing import Dict

class SettingsService:
    @staticmethod
    def get_api_key_status() -> Dict:
        """Check if API key is configured"""
        api_key = Settings.get_api_key()
        if api_key:
            # Return masked key for security
            masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"
            return {
                "configured": True,
                "maskedKey": masked_key
            }
        return {
            "configured": False,
            "maskedKey": None
        }
    
    @staticmethod
    def save_api_key(api_key: str) -> Dict:
        """Save API key to configuration"""
        if not api_key or len(api_key) < 10:
            raise ValueError("Invalid API key format")
        
        success = Settings.save_api_key(api_key)
        if success:
            return {
                "success": True,
                "message": "API key saved successfully"
            }
        raise Exception("Failed to save API key")
    
    @staticmethod
    def delete_api_key() -> Dict:
        """Delete API key from configuration"""
        success = Settings.delete_api_key()
        if success:
            return {
                "success": True,
                "message": "API key deleted successfully"
            }
        raise Exception("Failed to delete API key")

settings_service = SettingsService()
