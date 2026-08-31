from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "Agentic AI Revenue Recovery"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")

    RAZORPAY_KEY_ID: str = os.getenv("RAZORPAY_KEY_ID", "")
    RAZORPAY_KEY_SECRET: str = os.getenv("RAZORPAY_KEY_SECRET", "")

    MAX_RETRIES_PER_PAYMENT: int = int(os.getenv("MAX_RETRIES_PER_PAYMENT", "3"))
    COOLDOWN_MINUTES: int = int(os.getenv("COOLDOWN_MINUTES", "60"))
    MAX_AUTO_APPROVAL_AMOUNT: float = float(os.getenv("MAX_AUTO_APPROVAL_AMOUNT", "5000"))
    HUMAN_APPROVAL_THRESHOLD: float = float(os.getenv("HUMAN_APPROVAL_THRESHOLD", "5000"))

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()