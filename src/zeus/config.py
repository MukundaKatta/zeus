"""Configuration management for Zeus."""

from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import Field


class ZeusConfig(BaseSettings):
    """Zeus application configuration."""

    model_config = {"env_prefix": "ZEUS_", "env_file": ".env"}

    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")
    default_model: str = Field(default="gpt-4", alias="DEFAULT_MODEL")
    output_dir: Path = Field(default=Path("./generated"), alias="OUTPUT_DIR")

    def get_output_path(self, project_name: str) -> Path:
        """Return the full output path for a project."""
        return self.output_dir / project_name


def load_config() -> ZeusConfig:
    """Load configuration from environment and .env file."""
    return ZeusConfig()
