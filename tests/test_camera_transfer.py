import logging
import os
from datetime import datetime
from pathlib import Path

import pytest

from camera_transfer import app
from camera_transfer.camera_file_getter import CameraFileGetter
from camera_transfer.camera_transfer import CameraTransfer
from camera_transfer.dotenv_config import Settings
from camera_transfer.hash_store import HashStore
from camera_transfer.os_file_getter import OSFileGetter
from camera_transfer.os_output_file_writer import OSOutputFileWriter

logger = logging.getLogger(__name__)


@pytest.fixture
def base_test_settings(tmp_path: Path) -> Settings:
    return Settings(
        camera_folder=tmp_path,
        main_photos_folder=tmp_path,
        main_videos_folder=tmp_path,
        sqlite_database=None,
        camera_model_short_names={"COOLPIX S9700": "S9700"},
        dry_run=False,
        log_level="DEBUG",
    )


@pytest.fixture
def single_image_test_settings(base_test_settings: Settings) -> Settings:
    base_test_settings.camera_folder = Path(__file__).parent / "DCIM/single_image"
    return base_test_settings


@pytest.fixture
def duplicate_image_test_settings(base_test_settings: Settings) -> Settings:
    base_test_settings.camera_folder = Path(__file__).parent / "DCIM/duplicate_image"
    return base_test_settings


@pytest.fixture
def single_video_test_settings(base_test_settings: Settings) -> Settings:
    base_test_settings.camera_folder = Path(__file__).parent / "DCIM/single_video"
    return base_test_settings


@pytest.fixture
def duplicate_video_test_settings(base_test_settings: Settings) -> Settings:
    base_test_settings.camera_folder = Path(__file__).parent / "DCIM/duplicate_video"
    return base_test_settings


@pytest.fixture
def all_files_test_settings(base_test_settings: Settings, tmp_path: Path) -> Settings:
    sqlite_file = tmp_path / "test.db"
    sqlite_file.touch(exist_ok=False)
    base_test_settings.camera_folder = Path(__file__).parent / "DCIM"
    base_test_settings.sqlite_database = sqlite_file

    return base_test_settings


def test_app_load_dotenv() -> None:
    settings = app.load_settings_from_dotenv(Path(__file__).parent / "test.env")

    assert settings.dry_run == False
    assert settings.camera_model_short_names == {"COOLPIX S9700": "S9700"}
    assert settings.main_photos_folder == Path("/tmp")
    assert settings.main_videos_folder == Path("/tmp")
    assert settings.camera_folder == Path("/tmp")
    assert settings.sqlite_database is None
    assert settings.image_formats == {".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG"}
    assert settings.video_formats == {".mov", ".MOV", ".mp4", ".MP4"}
    assert settings.log_level == "DEBUG"


##########################################################################################


def test_camera_transfer(single_image_test_settings: Settings) -> None:
    camera_transfer = app.get_camera_transfer_operation(single_image_test_settings)

    device_file_name = "DSCN6228.JPG"
    file_last_modified = datetime(2024, 1, 25, 16, 53, 49)
    os.utime(
        Path(single_image_test_settings.camera_folder) / device_file_name,
        (file_last_modified.timestamp(), file_last_modified.timestamp()),
    )

    camera_transfer.run()
    assert len(list(single_image_test_settings.main_photos_folder.iterdir())) == 1

    expected_output_file = (
        Path(single_image_test_settings.main_photos_folder)
        / datetime.now().strftime("%Y")
        / datetime.now().strftime("%m")
        / "2022-07-27T115409_S9700_6228.JPG"
    )
    assert expected_output_file.exists()
    assert expected_output_file.stat().st_size == 3560217

    mtime = expected_output_file.stat().st_mtime
    assert (
        datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        == "2024-01-25 16:53:49"
    )


def test_unknown_camera(single_image_test_settings: Settings) -> None:
    single_image_test_settings.camera_model_short_names = {}
    camera_transfer = app.get_camera_transfer_operation(single_image_test_settings)

    with pytest.raises(KeyError):
        camera_transfer.run()


def test_camera_transfer_duplicate(duplicate_image_test_settings: Settings) -> None:
    camera_transfer = app.get_camera_transfer_operation(duplicate_image_test_settings)
    camera_transfer.run()
    assert len(list(duplicate_image_test_settings.main_photos_folder.iterdir())) == 1

    expected_output_file = (
        Path(duplicate_image_test_settings.main_photos_folder)
        / datetime.now().strftime("%Y")
        / datetime.now().strftime("%m")
        / "2022-07-27T115409_S9700_6228.JPG"
    )
    assert expected_output_file.exists()
    assert expected_output_file.stat().st_size == 3560217


def test_video_transfer(single_video_test_settings: Settings) -> None:
    device_file_name = "blank_video.mp4"
    file_last_modified = datetime(2024, 1, 25, 17, 00, 3)
    os.utime(
        Path(single_video_test_settings.camera_folder) / device_file_name,
        (file_last_modified.timestamp(), file_last_modified.timestamp()),
    )

    camera_transfer = app.get_camera_transfer_operation(single_video_test_settings)
    camera_transfer.run()
    assert len(list(single_video_test_settings.main_videos_folder.iterdir())) == 1

    expected_output_file = (
        Path(single_video_test_settings.main_videos_folder)
        / datetime.now().strftime("%Y")
        / datetime.now().strftime("%m")
        / "2024-01-25T170003_video.mp4"
    )
    assert expected_output_file.exists()
    assert expected_output_file.stat().st_size == 1311047

    mtime = expected_output_file.stat().st_mtime
    assert (
        datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        == "2024-01-25 17:00:03"
    )


def test_video_transfer_duplicate(duplicate_video_test_settings: Settings) -> None:
    camera_transfer = app.get_camera_transfer_operation(duplicate_video_test_settings)
    device_file_name = "blank_video.mp4"

    file_last_modified = datetime(2024, 1, 25, 17, 00, 3)
    os.utime(
        Path(duplicate_video_test_settings.camera_folder) / device_file_name,
        (file_last_modified.timestamp(), file_last_modified.timestamp()),
    )
    camera_transfer.run()
    assert len(list(duplicate_video_test_settings.main_videos_folder.iterdir())) == 1

    expected_output_file = (
        Path(duplicate_video_test_settings.main_videos_folder)
        / datetime.now().strftime("%Y")
        / datetime.now().strftime("%m")
        / "2024-01-25T170003_video.mp4"
    )
    assert expected_output_file.exists()
    assert expected_output_file.stat().st_size == 1311047


def test_all_files_transfer(all_files_test_settings: Settings) -> None:
    camera_transfer = app.get_camera_transfer_operation(all_files_test_settings)
    camera_transfer.run()
    assert len(list(all_files_test_settings.main_photos_folder.glob("**/*.JPG"))) == 1
    assert len(list(all_files_test_settings.main_videos_folder.glob("**/*.mp4"))) == 1


def test_all_files_transfer_dry_run(all_files_test_settings: Settings) -> None:
    all_files_test_settings.dry_run = True
    camera_transfer = app.get_camera_transfer_operation(all_files_test_settings)
    camera_transfer.run()
    assert len(list(all_files_test_settings.main_photos_folder.glob("**/*.JPG"))) == 0
    assert len(list(all_files_test_settings.main_videos_folder.glob("**/*.mp4"))) == 0
