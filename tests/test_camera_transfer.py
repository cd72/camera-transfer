import pytest
from pathlib import Path
from cameratransfer.camera_transfer import CameraTransfer
from cameratransfer.dotenv_config import Settings

from cameratransfer.os_file_getter import OSFileGetter
from cameratransfer.os_output_file_writer import OSOutputFileWriter
from cameratransfer.hash_store import HashStore
from cameratransfer.camera_file_getter import CameraFileGetter
from datetime import datetime

import logging

logger = logging.getLogger(__name__)


@pytest.fixture
def single_image_test_settings(tmp_path):
    return Settings(
        CT_CAMERA_FOLDER=str(Path(__file__).parent / "DCIM/single_image"),
        CT_MAIN_PHOTOS_FOLDER=tmp_path,
        CT_SQLITE_DATABASE=":memory:",
        CT_DRY_RUN=False,
    )


def test_camera_transfer_new(single_image_test_settings):
    camera_transfer = CameraTransfer(
        camera_file_getter=CameraFileGetter(
            file_getter=OSFileGetter(
                location=single_image_test_settings.CAMERA_FOLDER,
                file_extensions={".jpg", ".JPG"},
                file_category="image",
            ),
            model_short_names={"COOLPIX S9700": "S9700"},
        ),
        output_file_writer=OSOutputFileWriter(
            base_location=single_image_test_settings.MAIN_PHOTOS_FOLDER
        ),
        hash_store=HashStore(filename=single_image_test_settings.SQLITE_DATABASE),
    )
    camera_transfer.run()
    assert len(list(single_image_test_settings.MAIN_PHOTOS_FOLDER.iterdir())) == 1

    expected_output_file = (
        Path(single_image_test_settings.MAIN_PHOTOS_FOLDER)
        / datetime.now().strftime("%Y")
        / datetime.now().strftime("%m")
        / "2022-07-27T115409_S9700_6228.JPG"
    )
    assert expected_output_file.exists()
    assert expected_output_file.stat().st_size == 3560217


@pytest.fixture
def single_image_os_file_getter(tmp_path):
    location = str(Path(__file__).parent / "DCIM/single_image")
    return OSFileGetter(
        location=location, file_extensions={".jpg", ".JPG"}, file_category="image"
    )


@pytest.fixture
def duplicate_image_os_file_getter():
    location = str(Path(__file__).parent / "DCIM/duplicate_image")
    return OSFileGetter(
        location=location, file_extensions={".jpg", ".JPG"}, file_category="image"
    )


@pytest.fixture
def single_video_os_file_getter():
    location = str(Path(__file__).parent / "DCIM/single_video")
    return OSFileGetter(
        location=location,
        file_extensions={".mov", ".MOV", ".mp4", ".MP4"},
        file_category="video",
    )


@pytest.fixture
def duplicate_video_os_file_getter():
    location = str(Path(__file__).parent / "DCIM/duplicate_video")
    return OSFileGetter(
        location=location,
        file_extensions={".mov", ".MOV", ".mp4", ".MP4"},
        file_category="video",
    )


@pytest.fixture
def single_image_camera_file_getter(single_image_os_file_getter):
    return CameraFileGetter(
        file_getter=single_image_os_file_getter,
        model_short_names={"COOLPIX S9700": "S9700"},
    )


@pytest.fixture
def duplicate_image_camera_file_getter(duplicate_image_os_file_getter):
    return CameraFileGetter(
        file_getter=duplicate_image_os_file_getter,
        model_short_names={"COOLPIX S9700": "S9700"},
    )


@pytest.fixture
def single_video_camera_file_getter(single_video_os_file_getter):
    return CameraFileGetter(
        file_getter=single_video_os_file_getter, model_short_names={}
    )


@pytest.fixture
def duplicate_video_camera_file_getter(duplicate_video_os_file_getter):
    return CameraFileGetter(
        file_getter=duplicate_video_os_file_getter, model_short_names={}
    )


@pytest.fixture
def temp_os_output_file_writer(tmp_path):
    return OSOutputFileWriter(base_location=tmp_path)


def test_camera_transfer(
    single_image_camera_file_getter, temp_os_output_file_writer, tmp_path
):
    camera_transfer_operation = CameraTransfer(
        camera_file_getter=single_image_camera_file_getter,
        output_file_writer=temp_os_output_file_writer,
        hash_store=HashStore(filename=":memory:"),
    )
    camera_transfer_operation.run()
    assert len(list(temp_os_output_file_writer.base_location.iterdir())) == 1

    expected_output_file = (
        Path(tmp_path)
        / datetime.now().strftime("%Y")
        / datetime.now().strftime("%m")
        / "2022-07-27T115409_S9700_6228.JPG"
    )
    assert expected_output_file.exists()
    assert expected_output_file.stat().st_size == 3560217


def test_camera_transfer_duplicate(
    duplicate_image_camera_file_getter, temp_os_output_file_writer, tmp_path
):
    camera_transfer_operation = CameraTransfer(
        camera_file_getter=duplicate_image_camera_file_getter,
        output_file_writer=temp_os_output_file_writer,
        hash_store=HashStore(filename=":memory:"),
    )
    camera_transfer_operation.run()
    assert len(list(temp_os_output_file_writer.base_location.iterdir())) == 1

    expected_output_file = (
        Path(tmp_path)
        / datetime.now().strftime("%Y")
        / datetime.now().strftime("%m")
        / "2022-07-27T115409_S9700_6228.JPG"
    )
    assert expected_output_file.exists()
    assert expected_output_file.stat().st_size == 3560217


def test_video_transfer(
    single_video_camera_file_getter, temp_os_output_file_writer, tmp_path
):
    camera_transfer_operation = CameraTransfer(
        camera_file_getter=single_video_camera_file_getter,
        output_file_writer=temp_os_output_file_writer,
        hash_store=HashStore(filename=":memory:"),
    )
    camera_transfer_operation.run()
    assert len(list(temp_os_output_file_writer.base_location.iterdir())) == 1

    expected_output_file = (
        Path(tmp_path)
        / datetime.now().strftime("%Y")
        / datetime.now().strftime("%m")
        / "2024-01-25T170003_video.mp4"
    )
    assert expected_output_file.exists()
    assert expected_output_file.stat().st_size == 1311047


def test_video_transfer_duplicate(
    duplicate_video_camera_file_getter, temp_os_output_file_writer, tmp_path
):
    camera_transfer_operation = CameraTransfer(
        camera_file_getter=duplicate_video_camera_file_getter,
        output_file_writer=temp_os_output_file_writer,
        hash_store=HashStore(filename=":memory:"),
    )
    camera_transfer_operation.run()
    assert len(list(temp_os_output_file_writer.base_location.iterdir())) == 1

    expected_output_file = (
        Path(tmp_path)
        / datetime.now().strftime("%Y")
        / datetime.now().strftime("%m")
        / "2024-01-25T170003_video.mp4"
    )
    assert expected_output_file.exists()
    assert expected_output_file.stat().st_size == 1311047
