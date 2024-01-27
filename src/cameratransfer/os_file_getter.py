from pathlib import Path
from cameratransfer.camera_file import CameraFile
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

    def get_next_file(self) -> Iterator[CameraFile]:
        for file in self.list_files():
            logger.info("in loop with file: %s", file)
            yield CameraFile(
                file_name=file.name,
                file_content=file.read_bytes(),
                file_last_modified=datetime.fromtimestamp(file.stat().st_mtime),
                file_category=self.file_category
            )

  
