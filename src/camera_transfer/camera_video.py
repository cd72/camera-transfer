from datetime import datetime
import logging
import hashlib
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class CameraVideo:
    file_name: str
    file_content: bytes
    file_last_modified: datetime
    file_category: str
    extra_fields: dict[str, dict[str, str]]

    def generate_new_file_name(self) -> str:
        logger.debug(self.file_name)
        logger.debug(self.file_last_modified)
        video_modification_time_string = self.file_last_modified.strftime(
            "%Y-%m-%dT%H%M%S"
        )
        return f"{video_modification_time_string}_video.mp4"

    def file_hash(self) -> bytes:
        return hashlib.sha256(self.file_content).digest()
