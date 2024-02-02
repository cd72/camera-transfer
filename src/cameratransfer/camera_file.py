import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

logger = logging.getLogger(__name__)

@dataclass
class CameraFile(Protocol):
    file_name: str
    file_content: bytes
    file_last_modified: datetime
    file_category: str
    extra_fields: dict[str, dict[str, str]]

    def file_hash(self) -> bytes:
        ...

    def generate_new_file_name(self) -> str:
        ...
