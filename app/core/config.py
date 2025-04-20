import os
from typing import Any, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

from pydantic import field_validator, computed_field, ConfigDict, BaseModel


class Settings(BaseModel):
    model_config = ConfigDict(case_sensitive=True)
    
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI PostgreSQL App"
    
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "fastapi_db")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    
    @computed_field
    @property
    def DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
API_V1_STR = settings.API_V1_STR