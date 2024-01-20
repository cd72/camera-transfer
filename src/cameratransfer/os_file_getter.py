from pathlib import Path
from cameratransfer.file_data import FileData
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

    def get_next_file(self) -> Iterator[FileData]:
        logger.info("in get_next_file")
        for file in self.list_files():
            logger.info("in loop with file: %s", file)
            yield FileData(
                file_name=file.name,
                file_bytes=file.read_bytes(),
                file_extension=file.suffix,
                file_last_modified=datetime.fromtimestamp(file.stat().st_mtime),
                file_category=self.file_category
            )

  
