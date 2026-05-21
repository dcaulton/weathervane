from pydantic_settings import BaseSettings, SettingsConfigDict


class AgentSettings(BaseSettings):
    """All configuration for the Weathervane agent."""

    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

    # LLM settings (we'll use vLLM running locally on 1080Ti)
    llm_model: str = "meta-llama/Llama-3.1-70B-Instruct"  # or whatever you're running
    llm_base_url: str = "http://localhost:8000/v1"  # vLLM OpenAI-compatible endpoint
    llm_temperature: float = 0.3

    # External services
    openmeteo_url: str = "https://api.open-meteo.com/v1"
    github_token: str | None = None
    github_repo: str = "yourusername/weathervane"  # for Obsidian notes

    # Postgres
    database_url: str = "postgresql+psycopg2://user:pass@localhost:5432/weathervane"


settings = AgentSettings()
