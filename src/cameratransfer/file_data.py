from dataclasses import dataclass
from datetime import datetime

@dataclass
class FileData():
    file_name: str
    file_bytes: bytes
    file_extension: str
    file_last_modified: datetime
    file_category: str

