"""Application configuration settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_env: str = "development"
    debug: bool = False

    # Database
    database_url: str
    database_pool_size: int = 10

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # AI Services
    openai_api_key: str
    anthropic_api_key: str
    runway_api_key: str

    # Storage (AWS S3)
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str = "us-east-1"
    s3_bucket_name: str

    # Celery
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"

    # Application Settings
    max_script_length: int = 10000
    max_video_duration: int = 300
    output_video_format: str = "mp4"
    output_video_resolution: str = "1920x1080"
    output_video_fps: int = 30

    # Security
    secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


settings = Settings()
