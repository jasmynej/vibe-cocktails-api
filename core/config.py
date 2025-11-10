from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_URI: str = 'postgresql://jasmynejean-remy@localhost:5432/vibe-cocktails'
    OPEN_AI_KEY: str
    SUPABASE_SERVICE_ROLE: str
    SUPABASE_PROJECT_ID: str
    SUPABASE_PWD: str
    SUPABASE_URI: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_S3_BUCKET: str
    AWS_REGION: str
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
