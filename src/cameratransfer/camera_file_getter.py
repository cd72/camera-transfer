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


file_type_mapping = {
    ".jpg": "image",
    ".jpeg": "image",
    ".JPG": "image",
    ".JPEG": "image",
    ".mov": "video",
    ".MOV": "video",
    ".mp4": "video",
    ".MP4": "video",
    ".png": "image",
    ".PNG": "image"
    # TODO: Add more
    # ".mp3": "audio",
    # ".MP3": "audio"
}

dispatch_table: dict[str, type[CameraFile]] = {
    "image": CameraImage,
    "video": CameraVideo       
}


@dataclass
class CameraFileGetter:
    file_getter: FileGetter
    model_short_names: dict[str, str]

    def get_next_file(self) -> Iterator[CameraFile]:
        for file in self.file_getter.get_next_file():
            file_suffix = Path(file.file_name).suffix
            logger.debug("File suffix: %s", file_suffix)
            file_category = file_type_mapping[file_suffix]
            logger.debug("File category: %s", file_category)
            CameraFileClass = dispatch_table[file_category]

            yield CameraFileClass(
                file_name=file.file_name,
                file_content=file.file_content,
                file_last_modified=file.file_last_modified,
                file_category=file_category,
                extra_fields={"model_short_names": self.model_short_names}
            )