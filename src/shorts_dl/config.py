from __future__ import annotations

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the downloader service."""

    app_name: str = "shorts-download1121"
    downloads_dir: Path = Path("downloads")
    default_batch_videos: int = 5
    min_batch_videos: int = 1
    max_batch_videos: int = 20

    model_config = SettingsConfigDict(
        env_prefix="SHORTS_DL_",
        env_file=".env",
        case_sensitive=False,
    )


settings = Settings()
settings.downloads_dir.mkdir(parents=True, exist_ok=True)
