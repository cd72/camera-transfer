from pathlib import Path

from pydantic import DirectoryPath, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings, validate_assignment=True):
    dry_run: bool = Field(validation_alias='CT_DRY_RUN')
    camera_folder: DirectoryPath = Field(validation_alias='CT_CAMERA_FOLDER')
    main_photos_folder: DirectoryPath = Field(validation_alias='CT_MAIN_PHOTOS_FOLDER')
    sqlite_database: Path = Field(validation_alias='CT_SQLITE_DATABASE')
    camera_model_short_names: dict[str, str] = Field(validation_alias='CT_CAMERA_MODEL_SHORT_NAMES')
 
    # model_config = SettingsConfigDict(env_file='/mnt/d/projects/camera-transfer/tests/test.env')
    # model_config = SettingsConfigDict()


