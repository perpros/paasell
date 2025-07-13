from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    admin_email: str


settings = Settings()
