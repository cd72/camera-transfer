from typing import Protocol, Iterator
from datetime import datetime
from dataclasses import dataclass
from cameratransfer.camera_file import CameraFile
import logging

logger = logging.getLogger(__name__)

class CameraFileGetter(Protocol):
    def get_next_file(self) -> Iterator[CameraFile]:
        ...

class OutputFileWriter(Protocol):
    def write_file(self, file_name: str, file_last_modified: datetime) -> None:
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
        logger.debug("Processing camera file %s", camera_file.file_name)

        if camera_file.file_hash() in self.hash_store:
            logger.debug("Skipping duplicate camera file")
            return

        new_file_name = camera_file.generate_new_file_name()
        new_last_modified = camera_file.file_last_modified
        logger.debug(new_file_name)
        self.output_file_writer.write_file(new_file_name, new_last_modified)
        self.hash_store[camera_file.file_hash()] = new_file_name

    def run(self) -> None:
        logger.debug("Running Camera Transfer")
        for camera_file in self.camera_file_getter.get_next_file():
            self.process_camera_file(camera_file)
