from pathlib import Path
from camera_transfer.camera_file import CameraFile
from camera_transfer.camera_file_getter import File
from typing import Iterator
from datetime import datetime
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class OSFileGetter:
    location: Path
    file_extensions: set[str]

    def list_files(self) -> Iterator[Path]:
        logger.info("Listing files in location: %s", self.location)
        return (p.resolve() for p in self.location.glob("**/*") if p.suffix in self.file_extensions)

    def get_next_file(self) -> Iterator[File]:
        for file in self.list_files():
            logger.debug("in list_files loop with file: %s", file.relative_to(self.location))
            yield File(
                file.name, 
                file.read_bytes(),
                datetime.fromtimestamp(file.stat().st_mtime)
            )

  
