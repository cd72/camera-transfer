from pathlib import Path

from pydantic import DirectoryPath, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings, validate_assignment=True):
    dry_run: bool
    camera_folder: DirectoryPath
    main_photos_folder: DirectoryPath
    sqlite_database: Path | None = None
    camera_model_short_names: dict[str, str]

    # model_config = SettingsConfigDict(env_file='/mnt/d/projects/camera-transfer/tests/test.env')
    model_config = SettingsConfigDict(env_prefix="CT_")
