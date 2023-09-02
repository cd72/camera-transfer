from pathlib import Path

from pydantic import DirectoryPath, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    camera_folder: DirectoryPath = Field(validation_alias='CT_CAMERA_FOLDER')
    photos_folder: DirectoryPath = Field(validation_alias='CT_PHOTOS_FOLDER')
    sqlite_database: Path = Field(validation_alias='CT_SQLITE_DATABASE')
    model_config = SettingsConfigDict(env_file='.env', extra='forbid')
    # model_config = SettingsConfigDict(env_file='.env', extra='forbid', env_prefix='CT_')

print("parsing settings...")
settings = Settings()
