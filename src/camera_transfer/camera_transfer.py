from typing import Protocol, Iterator
from datetime import datetime
from dataclasses import dataclass
from camera_transfer.camera_file import CameraFile
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class CameraFileGetter(Protocol):
    def get_next_file(self) -> Iterator[CameraFile]:
        ...

class OutputFileWriter(Protocol):
    def write_file(self, file_name: str, file_last_modified: datetime, file_content: bytes, file_category: str, sub_folder: Path) -> None:
        ...


class HashStore(Protocol):
    def __setitem__(self, hash: bytes, file_item: str) -> None:
        ...

    def __contains__(self, hash: bytes) -> bool:
        ...

@dataclass
class CameraTransfer:
    camera_file_getter: CameraFileGetter
    output_file_writer: OutputFileWriter
    hash_store: HashStore

    def process_camera_file(self, camera_file: CameraFile) -> None:
        logger.info("Processing camera file %s", camera_file.file_name)

        if camera_file.file_hash() in self.hash_store:
            logger.info("Skipping duplicate camera file")
            return

        new_file_name = camera_file.generate_new_file_name()
        sub_folder = Path(datetime.now().strftime("%Y/%m"))
        logger.debug(new_file_name)
        self.output_file_writer.write_file(
            camera_file.generate_new_file_name(),
            camera_file.file_last_modified,
            camera_file.file_content,
            file_category=camera_file.file_category,
            sub_folder=sub_folder
            )
        logger.info("Wrote file %s", new_file_name)
        self.hash_store[camera_file.file_hash()] = camera_file.generate_new_file_name()

    def run(self) -> None:
        logger.debug("Running Camera Transfer")
        for camera_file in self.camera_file_getter.get_next_file():
            self.process_camera_file(camera_file)
