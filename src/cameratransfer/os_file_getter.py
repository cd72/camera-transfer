from pathlib import Path
from cameratransfer.camera_file import CameraFile
from cameratransfer.camera_file_getter import File
from typing import Iterator
from datetime import datetime
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class OSFileGetter:
    location: str
    file_extensions: set[str]

    def __post_init__(self):
        self.path = Path(self.location)

    def list_files(self) -> Iterator[Path]:
        return (p.resolve() for p in self.path.glob("**/*") if p.suffix in self.file_extensions)

    def get_next_file(self) -> Iterator[File]:
        for file in self.list_files():
            logger.info("in loop with file: %s", file)
            yield File(
                file.name, 
                file.read_bytes(),
                datetime.fromtimestamp(file.stat().st_mtime)
            )

  
