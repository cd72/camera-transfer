from pathlib import Path
from cameratransfer.camera_file import CameraFile
from cameratransfer.camera_file_getter import File
from typing import Iterator
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class OSFileGetter:
    def __init__(self, location: str, file_extensions: set[str], file_category: str) -> None:
        self.location = location
        self.file_extensions = file_extensions
        self.file_category = file_category
        self.path = Path(location)

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

  
