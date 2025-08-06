from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Charger les variables d’environnement
load_dotenv()

class Settings(BaseSettings):
    DB_URL: str = os.getenv("DB_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALLOWED_ORIGINS: list = ["*"]  # À adapter si besoin
    APP_ENV: str = os.getenv("APP_ENV", "production")  # Valeur par défaut

settings = Settings()

