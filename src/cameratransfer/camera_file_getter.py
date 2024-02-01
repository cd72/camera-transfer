from cameratransfer.camera_image import CameraImage
from cameratransfer.camera_video import CameraVideo
from cameratransfer.camera_file import CameraFile
from typing import Protocol, Iterator
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


@dataclass
class File:
    file_name: str
    file_content: bytes
    file_last_modified: datetime


class FileGetter(Protocol):
    def get_next_file(self) -> Iterator[File]:
        ...


@dataclass
class CameraFileGetter:
    file_getter: FileGetter
    model_short_names: dict[str, str]

    def get_next_file(self) -> Iterator[CameraFile]:
        for file in self.file_getter.get_next_file():
            file_suffix = Path(file.file_name).suffix
            if file_suffix in {".jpg", ".jpeg", ".JPG", ".JPEG"}:
                yield CameraImage(
                    file_name=file.file_name,
                    file_content=file.file_content,
                    file_last_modified=file.file_last_modified,
                    file_category="image",
                    model_short_names=self.model_short_names
                )
            elif file_suffix in {".mov", ".MOV", ".mp4", ".MP4"}:
                yield CameraVideo(
                    file_name=file.file_name,
                    file_content=file.file_content,
                    file_last_modified=file.file_last_modified,
                    file_category="video",
                )
            else:
                logger.warning("Unknown file type: %s", file_suffix)
                raise NotImplementedError
