import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterator, Protocol

from cameratransfer.camera_file import CameraFile
from cameratransfer.camera_image import CameraImage
from cameratransfer.camera_video import CameraVideo

logger = logging.getLogger(__name__)


@dataclass
class File:
    file_name: str
    file_content: bytes
    file_last_modified: datetime


class FileGetter(Protocol):
    def get_next_file(self) -> Iterator[File]:
        ...



dispatch_table: dict[str, type[CameraFile]] = {
    "image": CameraImage,
    "video": CameraVideo       
}


@dataclass
class CameraFileGetter:
    file_getter: FileGetter
    camera_model_short_names: dict[str, str]
    image_formats: set[str]
    video_formats: set[str]

    def __post_init__(self) -> None:
        image_category = { image_format: "image" for image_format in self.image_formats }
        video_category = { video_format: "video" for video_format in self.video_formats }
        self.file_category_lookup = { **image_category, **video_category }


    def get_next_file(self) -> Iterator[CameraFile]:
        for file in self.file_getter.get_next_file():
            file_suffix = Path(file.file_name).suffix
            logger.debug("File suffix: %s", file_suffix)
            file_category = self.file_category_lookup[file_suffix]
            logger.debug("File category: %s", file_category)
            CameraFileClass = dispatch_table[file_category]

            yield CameraFileClass(
                file_name=file.file_name,
                file_content=file.file_content,
                file_last_modified=file.file_last_modified,
                file_category=file_category,
                extra_fields={"camera_model_short_names": self.camera_model_short_names}
            )