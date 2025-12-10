import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = os.getenv("APP_NAME", "Fibo Project")
    VERSION: str = os.getenv("API_VERSION", "v1")
    
settings = Settings()