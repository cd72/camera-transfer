from pathlib import Path

from pydantic import DirectoryPath, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DRY_RUN: bool = Field(validation_alias='CT_DRY_RUN')
    camera_folder: DirectoryPath = Field(validation_alias='CT_CAMERA_FOLDER')
    main_photos_folder: DirectoryPath = Field(validation_alias='CT_MAIN_PHOTOS_FOLDER')
    sqlite_database: Path = Field(validation_alias='CT_SQLITE_DATABASE')
    model_config = SettingsConfigDict(env_file='.env', extra='forbid')
    # model_config = SettingsConfigDict(env_file='.env', extra='forbid', env_prefix='CT_')

print("parsing settings...")
config = Config()
