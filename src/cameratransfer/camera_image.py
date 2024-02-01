import exif # type: ignore
import hashlib
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

@dataclass
class CameraImage():
    file_name: str
    file_content: bytes
    file_last_modified: datetime
    file_category: str
    extra_fields: dict[str, dict[str, str]]
    
    def __post_init__(self) -> None:
        self._exif = exif.Image(self.file_content)
        self._model_short_names = self.extra_fields["model_short_names"]


    def generate_new_file_name(self):
        filename, file_extension = os.path.splitext(self.file_name)
        return (
            f"{self.condensed_date_string}_"
            f"{self.model_short_name()}_"
            f"{self.get_image_file_name_digits()}"
            f"{file_extension}"
        )

    def file_hash(self) -> bytes:
        return hashlib.sha256(self.file_content).digest()

    def get_image_file_name_digits(self) -> str:
        digits = "".join([n for n in self.file_name if n.isdigit()])
        logger.debug(f"digits           : {digits}")
        logger.debug(f"datetime_digits  : {self.datetime_digits}")
        digits = digits.replace(self.datetime_digits, "")
        digits = digits.replace(str(int(self.datetime_digits)+1), "")
        digits = digits.replace(str(int(self.datetime_digits)-1), "")
        digits = "0" if digits == "" else digits
        logger.debug(f"digits           : {digits}")
        return digits

    def model(self) -> str:
        return self._exif.get("model").strip()


    def model_short_name(self) -> str:
        return self._model_short_names[self.model()]

    @property
    def condensed_date_string(self) -> str:
        logger.debug(self.datetime_string)
        return self.datetime_string.replace(":", "-", 2).replace(":", "", 2).replace(" ", "T")

    @property
    def datetime_digits(self) -> str:
        return "".join([n for n in self.datetime_string if n.isdigit()])

    @property
    def datetime_string(self) -> str:
        return self._exif.get("datetime")

