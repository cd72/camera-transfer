from pathlib import Path

from pydantic import DirectoryPath, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings, validate_assignment=True):
    DRY_RUN: bool = Field(validation_alias='CT_DRY_RUN')
    CAMERA_FOLDER: DirectoryPath = Field(validation_alias='CT_CAMERA_FOLDER')
    MAIN_PHOTOS_FOLDER: DirectoryPath = Field(validation_alias='CT_MAIN_PHOTOS_FOLDER')
    SQLITE_DATABASE: Path = Field(validation_alias='CT_SQLITE_DATABASE')
    # DRY_RUN: bool
    # CAMERA_FOLDER: DirectoryPath
    # MAIN_PHOTOS_FOLDER: DirectoryPath
    # SQLITE_DATABASE: Path
    # model_config = SettingsConfigDict(env_file='.env', extra='forbid')

    # def my_get_config(self, *args, **kwargs):
    #     print("parsing settings...")
    #     return Config(args, kwargs)

