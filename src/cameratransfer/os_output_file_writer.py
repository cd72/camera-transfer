import logging
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
import os

logger = logging.getLogger(__name__)

@dataclass
class OSOutputFileWriter:
    base_image_location: Path
    base_video_location: Path
    dry_run: bool = False

    def write_file(self, file_name: str, file_last_modified: datetime, file_content: bytes, file_category: str, sub_folder: Path) -> None:
        logger.debug(f"file_name: {file_name}")
        logger.debug(f"file_last_modified: {file_last_modified}")
        if file_category == "image":
            fq_file_name = self.base_image_location.joinpath(sub_folder, file_name)
        elif file_category == "video":
            fq_file_name = self.base_video_location.joinpath(sub_folder, file_name)
        
        if self.dry_run:
            logger.debug(f"Would write to file: {fq_file_name}")
            return

        logger.debug(f"Writing to file: {fq_file_name}")
        fq_file_name.parent.mkdir(parents=True, exist_ok=True)
        fq_file_name.touch(exist_ok=False)
        fq_file_name.write_bytes(file_content)

        os.utime(fq_file_name, (file_last_modified.timestamp(), file_last_modified.timestamp()))