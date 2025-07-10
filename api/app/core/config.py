import secrets
from typing import List, Union, Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import validator, PostgresDsn, HttpUrl

class Settings(BaseSettings):
    PROJECT_NAME: str = "B2B2C Wholesale Platform API"
    API_V1_STR: str = "/api/v1"

    # JWT settings
    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database settings
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: Union[PostgresDsn, str] = ""

    @validator("DATABASE_URL", pre=True, always=True)
    def assemble_db_connection(cls, v: Union[str, None], values: dict[str, Any]) -> Any:
        if isinstance(v, str) and v:
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # CORS settings
    BACKEND_CORS_ORIGINS: List[HttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[HttpUrl], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Environment specific settings
    # For local development, Pydantic will load .env file by default if python-dotenv is installed.
    # Ensure .env file is in the root of the `api` directory when running with uvicorn locally,
    # or that environment variables are set in docker-compose.yml
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")


settings = Settings()
