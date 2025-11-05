from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URI: str = 'postgresql://jasmynejean-remy@localhost:5432/vibe-cocktails'

settings = Settings()
