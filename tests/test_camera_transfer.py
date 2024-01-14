import pytest

from camera_transfer.camera_transfer import CameraTransfer
from camera_transfer.dotenv_config import Settings

@pytest.fixture
def settings_dry_run():
    settings_dict = {
        "CT_CAMERA_FOLDER": "/mnt/d/projects/camera-transfer/tests/DCIM",
        "CT_MAIN_PHOTOS_FOLDER": "/home/chris/Pictures/photos",
        "CT_SQLITE_DATABASE": "/mnt/d/projects/camera-transfer/development/version03/image_hashes.db",
        "CT_DRY_RUN": True
    }
    return Settings(**settings_dict)


def test_basic(settings_dry_run: Settings):
    transfer = CameraTransfer(settings_dry_run)
    assert transfer.transfer_photos()

    
    