import exif # type: ignore
import hashlib
import logging
import os

logger = logging.getLogger(__name__)

class CameraImage:

    def __init__(self, image_bytes: bytes, image_basename: str, model_short_names: dict):
        self.image_bytes = image_bytes
        self.image_basename = image_basename
        self.model_short_names = model_short_names
        self._exif = exif.Image(self.image_bytes)
    

    def generate_new_file_name(self):
        filename, file_extension = os.path.splitext(self.image_basename)
        return (
            f"{self.condensed_date_string}_"
            f"{self.model_short_name}_"
            f"{self.get_image_file_name_digits()}"
            f"{file_extension}"
        )


    @property
    def image_hash(self) -> bytes:
        return hashlib.sha256(self.image_bytes).digest()

    def get_image_file_name_digits(self) -> str:
        digits = "".join([n for n in self.image_basename if n.isdigit()])
        logger.debug(f"digits           : {digits}")
        logger.debug(f"datetime_digits  : {self.datetime_digits}")
        digits = digits.replace(self.datetime_digits, "")
        digits = digits.replace(str(int(self.datetime_digits)+1), "")
        digits = digits.replace(str(int(self.datetime_digits)-1), "")
        digits = "0" if digits == "" else digits
        logger.debug(f"digits           : {digits}")
        return digits

    # @property
    # def make(self) -> str:
    #     return self._exif.get("make").strip()

    @property
    def model(self) -> str:
        return self._exif.get("model").strip()

    @property
    def model_short_name(self) -> str:
        return self.model_short_names[self.model]

    @property
    def condensed_date_string(self) -> str:
        logger.debug(self.datetime_string)
        return self.datetime_string.replace(":", "-", 2).replace(":", "", 2).replace(" ", "T")

    @property
    def datetime_digits(self) -> str:
        return "".join([n for n in self.datetime_string if n.isdigit()])

    # @property
    # def software(self) -> str:
    #     return self._exif.get("software").strip()

    @property
    def datetime_string(self) -> str:
        return self._exif.get("datetime")

    # @property
    # def focal_length(self) -> float:
    #     return self._exif.get("focal_length")

    # @property
    # def f_number(self) -> float:
    #     return self._exif.get("f_number")

    # @property
    # def exposure_time(self) -> float:
    #     return self._exif.get("exposure_time")

    # @property
    # def photographic_sensitivity(self) -> int:
    #     return self._exif.get("photographic_sensitivity")

    # def all_info(self) -> dict:
    #     return dict(
    #         image_basename=self.image_basename,
    #         make=self.make,
    #         model=self.model,
    #         model_short_name=self.model_short_name,
    #         software=self.software,
    #         datetime_string=self.datetime_string,
    #         condensed_date_string=self.condensed_date_string,
    #         focal_length=self.focal_length,
    #         f_number=self.f_number,
    #         exposure_time=self.exposure_time,
    #         photographic_sensitivity=self.photographic_sensitivity,
    #         image_file_name_digits=self.get_image_file_name_digits(),
    #     )
