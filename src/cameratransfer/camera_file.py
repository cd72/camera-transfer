import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

logger = logging.getLogger(__name__)

class CameraFile(Protocol):
    file_name: str
    file_content: bytes
    file_last_modified: datetime
    file_category: str

    def file_hash(self) -> bytes:
        ...

    def generate_new_file_name(self) -> str:
        ...