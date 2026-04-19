import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = "TalentScout Hiring Assistant"
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")
    MAX_TECH_QUESTIONS: int = 5
    MIN_TECH_QUESTIONS: int = 3


settings = Settings()