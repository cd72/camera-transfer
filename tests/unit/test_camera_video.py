import pytest
import logging
import os
from pathlib import Path
from cameratransfer import camera_video
logger = logging.getLogger(__name__)



@pytest.fixture
def test_image(get_file_bytes, model_shortnames):
    test_file_name = "DCIM/100NIKON/DSCN6228.JPG"
    test_image = camera_image.CameraImage(
        get_file_bytes(test_file_name),
        os.path.basename(test_file_name),
        model_shortnames=model_shortnames,
    )
    return test_image

