import hashlib
import logging
import re
from datetime import date
from functools import cache, cached_property
from pathlib import Path

import exif  # type: ignore

from camera_transfer.hash_store import HashStore
from camera_transfer.dotenv_config import config
import shutil

logger = logging.getLogger(__name__)


def skip_on_dry_run(func):
    def wrapper(*args, **kwargs):
        if config.DRY_RUN:
            (self, *other_args) = args
            logger.debug(
                f"Dry-run mode enabled for {func.__name__}, {other_args} No changes will be made."
            )
            return  # Exit without executing the decorated function
        return func(*args, **kwargs)

    return wrapper


class CameraImage:
    def __init__(self, image_path: Path):
        self.image_path = image_path

    # cache the result of the next method
    @cache
    def get_image_content(self):
        return self.image_path.read_bytes()

    def __repr__(self):
        return f"CameraImage({self.image_path})"

    def __str__(self):
        return f"CameraImage({self.image_path})"

    def generate_new_file_name(self):
        return (
            f"{self.condensed_date_string}_"
            f"{self.model_short_name}_"
            f"{self.image_file_name_digits}_"
            f"{self.image_path.suffix}"
        )

    @cached_property
    def image_exif(self):
        image_content = self.get_image_content()
        return exif.Image(image_content)

    @property
    def image_hash(self):
        return hashlib.sha256(self.get_image_content()).digest()

    @property
    def image_file_name_digits(self):
        digits = "".join([n for n in self.image_path.name if n.isdigit()])
        digits.replace(self.datetime_digits, "")
        logger.debug(f"digits         : {digits}")
        logger.debug(f"datetime_digits: {self.datetime_digits}")
        return digits

    @property
    def make(self):
        return self.image_exif.get("make")

    @property
    def model(self):
        return self.image_exif.get("model").strip()

    @property
    def model_short_name(self):
        match self.model:
            case "COOLPIX S9700":
                return "S9700"
            case "Canon IXUS 115 HS":
                return "IXUS115HS"
            case "NIKON Z fc":
                return "ZFC"
            case "TFY-LX1":
                return "X8C"
            case _:
                raise ValueError("unrecognized camera model", self.model)

    @property
    def condensed_date_string(self):
        return self.datetime.replace(":", "-", 2).replace(":", "", 2).replace(" ", "T")

    @property
    def datetime_digits(self):
        return "".join([n for n in self.datetime if n.isdigit()])

    @property
    def software(self):
        return self.image_exif.get("software").strip()

    @property
    def datetime(self):
        return self.image_exif.get("datetime")

    @property
    def focal_length(self):
        return self.image_exif.get("focal_length")

    @property
    def f_number(self):
        return self.image_exif.get("f_number")

    @property
    def exposure_time(self):
        return self.image_exif.get("exposure_time")

    @property
    def photographic_sensitivity(self):
        return self.image_exif.get("photographic_sensitivity")

    @property
    def all_attributes(self):
        return dict(
            vars(self),
            make=self.make,
            model=self.model,
            model_short_name=self.model_short_name,
            software=self.software,
            datetime=self.datetime,
            condensed_date_string=self.condensed_date_string,
            focal_length=self.focal_length,
            f_number=self.f_number,
            exposure_time=self.exposure_time,
            photographic_sensitivity=self.photographic_sensitivity,
            image_file_name_digits=self.image_file_name_digits,
        )


class CameraTransfer:
    def __init__(
        self,
        camera_folder: Path,
        main_photos_folder: Path,
        sqlite_database: Path,
        dry_run: bool,
    ):
        self.camera_folder = camera_folder
        self.main_photos_folder = main_photos_folder
        self.sqlite_database = sqlite_database
        self.image_hashes = HashStore(sqlite_database)
        self.dry_run = dry_run

    def get_photo_loading_folder(self):
        today = date.today()
        day = today.strftime("%d")
        month = today.strftime("%m") + " - " + today.strftime("%B")
        year = today.strftime("%Y")

        today_folder = self.main_photos_folder / year / month / day
        today_folder.mkdir(parents=True, exist_ok=True)
        return today_folder

    def all_camera_images(self):
        logger.debug(f"Listing all photos in {self.camera_folder}")
        image_file_types = [".jpg", ".jpeg", ".JPG", ".JPEG"]

        for path in self.camera_folder.rglob(r"**/*"):
            if path.suffix in image_file_types:
                yield CameraImage(path)

    @skip_on_dry_run
    def perform_copy_operation(self, source: Path, destination: Path):
        logger.debug(f"Copying fil {source} to file {destination}")
        destination.write_bytes(source.read_bytes())

    def transfer_image(self, image: CameraImage):
        logger.debug(f"Dry run: {self.dry_run}")
        logger.debug(image.all_attributes)
        logger.debug(image.generate_new_file_name())
        logger.debug(
            f"Copying {image} to {self.main_photos_folder}/{image.generate_new_file_name()}"
        )
        self.perform_copy_operation(
            image.image_path, self.main_photos_folder / image.generate_new_file_name()
        )

    def transfer_photos(self):
        for image in self.all_camera_images():
            self.transfer_image(image)

    def transfer_videos(self):
        pass
