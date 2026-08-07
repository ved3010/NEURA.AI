"""
Configuration — E.D.I.T.H. app-wide settings and environment keys.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Server identity
    SERVER_NAME: str = os.getenv("SERVER_NAME", "E.D.I.T.H.")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # API keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    SARVAM_API_KEY: str = os.getenv("SARVAM_API_KEY", "")
    DEEPGRAM_API_KEY: str = os.getenv("DEEPGRAM_API_KEY", "")


config = Config()
