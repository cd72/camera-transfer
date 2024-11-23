from pathlib import Path

from pydantic import DirectoryPath, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CameraSettings(BaseSettings, validate_assignment=True):
    camera_folder: DirectoryPath
    main_photos_folder: DirectoryPath
    main_videos_folder: DirectoryPath
    sqlite_database: Path | None = None
    camera_model_short_names: dict[str, str]
    image_formats: set[str] = Field(default_factory=lambda: {".jpg", ".JPG"})
    video_formats: set[str] = Field(default_factory=lambda: {".mov", ".MOV", ".mp4", ".MP4"})
    dry_run: bool
    log_level: str

    model_config = SettingsConfigDict(env_prefix="CT_", extra="forbid")
    
