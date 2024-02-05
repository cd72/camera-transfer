import logging
from datetime import datetime
from pathlib import Path

import pytest

from cameratransfer import app
from cameratransfer.camera_file_getter import CameraFileGetter
from cameratransfer.camera_transfer import CameraTransfer
from cameratransfer.dotenv_config import Settings
from cameratransfer.hash_store import HashStore
from cameratransfer.os_file_getter import OSFileGetter
from cameratransfer.os_output_file_writer import OSOutputFileWriter

logger = logging.getLogger(__name__)


@pytest.fixture
def single_image_test_settings(tmp_path: Path) -> Settings:
    return Settings(
        camera_folder=Path(__file__).parent / "DCIM/single_image",
        main_photos_folder=tmp_path,
        sqlite_database=None,
        dry_run=False,
        camera_model_short_names={"COOLPIX S9700": "S9700"},
    )


def test_app_load_dotenv() -> None:
    settings = app.load_settings_from_dotenv(Path(__file__).parent / "test.env")

    assert settings.dry_run == False
    assert settings.camera_model_short_names == {"COOLPIX S9700": "S9700"}
    assert settings.main_photos_folder == Path("/tmp")
    assert settings.camera_folder == Path("/tmp")
    assert settings.sqlite_database is None


@pytest.fixture
def single_image_os_file_getter() -> OSFileGetter:
    location = Path(__file__).parent / "DCIM/single_image"
    return OSFileGetter(location=location, file_extensions={".jpg", ".JPG"})


@pytest.fixture
def duplicate_image_os_file_getter() -> OSFileGetter:
    location = Path(__file__).parent / "DCIM/duplicate_image"
    return OSFileGetter(location=location, file_extensions={".jpg", ".JPG"})


@pytest.fixture
def single_video_os_file_getter() -> OSFileGetter:
    location = Path(__file__).parent / "DCIM/single_video"
    return OSFileGetter(
        location=location,
        file_extensions={".mov", ".MOV", ".mp4", ".MP4"},
    )


@pytest.fixture
def duplicate_video_os_file_getter() -> OSFileGetter:
    location = Path(__file__).parent / "DCIM/duplicate_video"
    return OSFileGetter(
        location=location,
        file_extensions={".mov", ".MOV", ".mp4", ".MP4"},
    )


@pytest.fixture
def single_image_camera_file_getter(
    single_image_os_file_getter: OSFileGetter,
) -> CameraFileGetter:
    return CameraFileGetter(
        file_getter=single_image_os_file_getter,
        camera_model_short_names={"COOLPIX S9700": "S9700"},
    )


@pytest.fixture
def duplicate_image_camera_file_getter(
    duplicate_image_os_file_getter: OSFileGetter,
) -> CameraFileGetter:
    return CameraFileGetter(
        file_getter=duplicate_image_os_file_getter,
        camera_model_short_names={"COOLPIX S9700": "S9700"},
    )


@pytest.fixture
def single_video_camera_file_getter(
    single_video_os_file_getter: OSFileGetter,
) -> CameraFileGetter:
    return CameraFileGetter(
        file_getter=single_video_os_file_getter, camera_model_short_names={}
    )


@pytest.fixture
def duplicate_video_camera_file_getter(
    duplicate_video_os_file_getter: OSFileGetter,
) -> CameraFileGetter:
    return CameraFileGetter(
        file_getter=duplicate_video_os_file_getter, camera_model_short_names={}
    )


@pytest.fixture
def temp_os_output_file_writer(tmp_path: Path) -> OSOutputFileWriter:
    return OSOutputFileWriter(base_location=tmp_path)

##########################################################################################


def test_camera_transfer_new(single_image_test_settings: Settings) -> None:
    camera_transfer = CameraTransfer(
        camera_file_getter=CameraFileGetter(
            file_getter=OSFileGetter(
                location=single_image_test_settings.camera_folder,
                file_extensions={".jpg", ".JPG"},
            ),
            camera_model_short_names=single_image_test_settings.camera_model_short_names,
        ),
        output_file_writer=OSOutputFileWriter(
            base_location=single_image_test_settings.main_photos_folder
        ),
        hash_store=HashStore(filename=single_image_test_settings.sqlite_database),
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


def test_camera_transfer(
    single_image_camera_file_getter: CameraFileGetter,
    temp_os_output_file_writer: OSOutputFileWriter,
    tmp_path: Path,
) -> None:
    camera_transfer_operation = CameraTransfer(
        camera_file_getter=single_image_camera_file_getter,
        output_file_writer=temp_os_output_file_writer,
        hash_store=HashStore(filename=None),
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
    duplicate_image_camera_file_getter: CameraFileGetter,
    temp_os_output_file_writer: OSOutputFileWriter,
    tmp_path: Path,
) -> None:
    camera_transfer_operation = CameraTransfer(
        camera_file_getter=duplicate_image_camera_file_getter,
        output_file_writer=temp_os_output_file_writer,
        hash_store=HashStore(filename=None),
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
    single_video_camera_file_getter: CameraFileGetter,
    temp_os_output_file_writer: OSOutputFileWriter,
    tmp_path: Path,
) -> None:
    camera_transfer_operation = CameraTransfer(
        camera_file_getter=single_video_camera_file_getter,
        output_file_writer=temp_os_output_file_writer,
        hash_store=HashStore(filename=None),
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
    duplicate_video_camera_file_getter: CameraFileGetter,
    temp_os_output_file_writer: OSOutputFileWriter,
    tmp_path: Path,
) -> None:
    camera_transfer_operation = CameraTransfer(
        camera_file_getter=duplicate_video_camera_file_getter,
        output_file_writer=temp_os_output_file_writer,
        hash_store=HashStore(filename=None),
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
