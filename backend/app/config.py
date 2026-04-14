from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://postgres:password@localhost:5432/aria"
    anthropic_api_key: str
    claude_model: str = "claude-sonnet-4-6"
    assistant_name: str = "Aria"
    user_name: str = "Irfan"
    max_context_docs: int = 5

    class Config:
        env_file = ".env"


settings = Settings()
