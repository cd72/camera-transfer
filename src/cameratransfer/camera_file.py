from dataclasses import dataclass
from datetime import datetime

@dataclass
class CameraFile():
    file_name: str
    file_content: bytes
    file_extension: str
    file_last_modified: datetime
    file_category: str

