import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Dynamically falls back to a local folder named 'logs' in the project root
    LOG_FILE_PATH: str = os.getenv("LOG_FILE_PATH", os.path.abspath("./logs/app_access.log"))
    ALERT_THRESHOLD: int = 4

settings = Settings()
