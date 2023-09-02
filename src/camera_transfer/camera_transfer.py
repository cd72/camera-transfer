import logging
from pathlib import Path
import exif  # type: ignore
import re
from functools import cached_property, cache
import hashlib



logger = logging.getLogger(__name__)


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
        # return re.search(r"\d+", self.image_path.name).group()
        return ''.join([n for n in self.image_path.name if n.isdigit()])

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
    


from camera_transfer.hash_store import HashStore

from datetime import date
class CameraTransfer:
    def __init__(self, camera_folder: Path, photos_folder: Path, sqlite_database: Path):
        self.camera_folder = camera_folder
        self.photos_folder = photos_folder
        self.sqlite_database = sqlite_database
        self.image_hashes = HashStore(sqlite_database)


    def get_photo_loading_folder(self):
        today = date.today()
        day = today.strftime("%d")
        month = today.strftime("%m") + " - " + today.strftime("%B")
        year = today.strftime("%Y")

        today_folder = self.photos_folder / year / month / day
        today_folder.mkdir(parents=True, exist_ok=True)
        return today_folder
    
    def all_camera_images(self):
        logger.debug(f"Listing all photos in {self.camera_folder}")
        image_file_types = [".jpg", ".jpeg", ".JPG", ".JPEG"]

        for path in self.camera_folder.rglob(r"**/*"):
            if path.suffix in image_file_types:
                yield CameraImage(path)

    def transfer_photos(self):
        for image in self.all_camera_images():
            logger.debug(f"Copying {image} to {self.photos_folder}")
            logger.debug(image.all_attributes)
            logger.debug(image.generate_new_file_name())

    def transfer_videos(self):
        pass
