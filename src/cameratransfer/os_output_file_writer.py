import logging
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class OSOutputFileWriter:
    base_location: Path
    sub_location: Path = Path(datetime.now().strftime("%Y/%m/%d"))

    def write_file(self, file_name: str, file_last_modified: datetime, file_content: bytes) -> None:
        logger.debug(f"file_name: {file_name}")
        logger.debug(f"file_last_modified: {file_last_modified}")
        fq_file_name = self.base_location.joinpath(self.sub_location, file_name)
        
        fq_file_name.parent.mkdir(parents=True, exist_ok=True)
        fq_file_name.touch(exist_ok=False)
        fq_file_name.write_bytes(file_content)
