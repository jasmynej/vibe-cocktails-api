from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_URI: str = 'postgresql://jasmynejean-remy@localhost:5432/vibe-cocktails'
    OPEN_AI_KEY: str
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
