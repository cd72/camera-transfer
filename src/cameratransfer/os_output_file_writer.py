import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class OSOutputFileWriter:
    def __init__(self, location: str):
        self.location = location

    def write_file(self, file_name: str, file_last_modified: datetime) -> None:
        logger.debug(f"file_name: {file_name}")
        logger.debug(f"file_last_modified: {file_last_modified}")
        Path(file_name).touch( exist_ok=True)