import pytest
import logging
import os
from pathlib import Path
from cameratransfer import camera_image
import hashlib

logger = logging.getLogger(__name__)


@pytest.fixture
def model_shortnames():
    return {
        "COOLPIX S9700": "S9700",
        "Canon IXUS 115 HS": "IXUS115HS",
        "NIKON Z fc": "ZFC",
        "TFY-LX1": "X8",
    }


@pytest.fixture
def test_image(get_file_bytes, model_shortnames):
    test_file_name = "DCIM/100NIKON/DSCN6228.JPG"
    test_image = camera_image.CameraImage(
        get_file_bytes(test_file_name),
        os.path.basename(test_file_name),
        model_shortnames=model_shortnames,
    )
    return test_image


@pytest.fixture
def phone_image(get_file_bytes, model_shortnames):
    phone_image_file_name = "DCIM/100NIKON/IMG_20230320_170719.jpg"
    phone_image = camera_image.CameraImage(
        get_file_bytes(phone_image_file_name),
        os.path.basename(phone_image_file_name),
        model_shortnames=model_shortnames,
    )
    return phone_image


def test_camera_image_instantiation(test_image):
    assert type(test_image) == camera_image.CameraImage


def test_image_hash(test_image):
    assert test_image.image_hash == bytes.fromhex(
        "73086ab6bf4d367825b43da443207af09c17123b4b79e3c239aa96649c50b341"
    )


def test_camera_make(test_image):
    assert test_image.make == "NIKON"


def test_camera_model(test_image):
    assert test_image.model == "COOLPIX S9700"


def test_camera_model_shortname(test_image):
    assert test_image.model_short_name == "S9700"


def test_image_datetime(test_image):
    assert test_image.datetime_string == "2022:07:27 11:54:09"


def test_focal_length(test_image):
    assert type(test_image.focal_length) == float
    assert test_image.focal_length == 6.4


def test_f_number(test_image):
    assert type(test_image.f_number) == float
    assert test_image.f_number == 4.0


def test_exposure_time(test_image):
    assert type(test_image.exposure_time) == float
    assert test_image.exposure_time == 0.001


def test_photographic_sensitivity(test_image):
    assert type(test_image.photographic_sensitivity) == int
    assert test_image.photographic_sensitivity == 125


def test_condensed_date_string(test_image):
    assert test_image.condensed_date_string == "2022-07-27T115409"


def test_datetime_digits(test_image):
    assert test_image.datetime_digits == "20220727115409"


def test_software(test_image):
    assert test_image.software == "COOLPIX S9700V1.0"


def test_get_image_file_name_digits(test_image):
    assert test_image.get_image_file_name_digits() == "6228"


def test_get_phone_image_file_name_digits(phone_image):
    assert phone_image.get_image_file_name_digits() == "0"


def test_camera_image_all_info(test_image):
    assert test_image.all_info() == {
        "image_basename": "DSCN6228.JPG",
        "make": "NIKON",
        "model": "COOLPIX S9700",
        "model_short_name": "S9700",
        "software": "COOLPIX S9700V1.0",
        "datetime_string": "2022:07:27 11:54:09",
        "condensed_date_string": "2022-07-27T115409",
        "focal_length": 6.4,
        "f_number": 4.0,
        "exposure_time": 0.001,
        "photographic_sensitivity": 125,
        "image_file_name_digits": "6228",
    }

def test_generate_new_file_name(test_image):
    assert test_image.generate_new_file_name() == "2022-07-27T115409_S9700_6228.JPG"

def test_generate_new_phone_image_file_name(phone_image):
    assert phone_image.generate_new_file_name() == "2023-03-20T170720_X8_0.jpg"

