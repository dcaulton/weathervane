from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AgentSettings(BaseSettings):
    """Weathervane Agent configuration.
    All values come from environment variables or .env file.
    Never commit real secrets.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
        # Fail fast if critical settings are missing
        env_file_encoding="utf-8",
    )

    # LLM (running locally on 1080Ti via vLLM)
    llm_model: str = "meta-llama/Llama-3.1-70B-Instruct"
    llm_base_url: str = "http://localhost:8000/v1"
    llm_temperature: float = 0.3

    # Postgres (required - no default)
    database_url: str = Field(
        ...,
        description="Full PostgreSQL connection string (use env var)",
        examples=["postgresql+psycopg2://user:pass@localhost:5432/weathervane"],
    )

    # Optional / external services
    openmeteo_url: str = "https://api.open-meteo.com/v1"
    github_token: str | None = None
    github_repo_owner: str | None = None
    github_repo_name: str | None = None


# Singleton instance
settings = AgentSettings()
