import os


class Config:
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
    # LLM Provider config
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')