from config import Settings

try:
    settings = Settings()
    print("Settings loaded successfully")
    print(f"Database URL: {settings.database_url}")
except Exception as e:
    print(f"Error loading settings: {e}")
