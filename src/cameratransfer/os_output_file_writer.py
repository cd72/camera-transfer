import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class OSOutputFileWriter:
    def __init__(self, location: Path):
        self.location: Path = location

    def write_file(self, file_name: str, file_last_modified: datetime, file_content: bytes) -> None:
        logger.debug(f"file_name: {file_name}")
        logger.debug(f"file_last_modified: {file_last_modified}")
        self.location.joinpath(file_name).touch(exist_ok=False)

        with open(self.location.joinpath(file_name), "wb") as f:
            f.write(file_content)