import pytest
from pathlib import Path
from cameratransfer.camera_transfer import CameraTransfer
from cameratransfer.camera_transfer import InputFileGetter
from cameratransfer.camera_transfer import OutputFileWriter
from cameratransfer.os_file_getter import OSFileGetter

from cameratransfer.hash_store import HashStore
from cameratransfer.file_data import FileData
from unittest import mock
from datetime import datetime


@pytest.fixture
def get_image(get_file_bytes, get_file_modification_time):
    test_file_name = "DCIM/100NIKON/DSCN6228.JPG"
    test_image = FileData(
        file_name=test_file_name,
        file_bytes=get_file_bytes(test_file_name),
        file_extension="JPG",
        file_last_modified=get_file_modification_time(test_file_name),
        file_category="image",
    )
    return test_image
@pytest.fixture
def get_video(get_file_bytes, get_file_modification_time):
    test_file_name = "DCIM/DSC_0246.MOV"
    test_image = FileData(
        file_name=test_file_name,
        file_bytes=get_file_bytes(test_file_name),
        file_extension="MOV",
        file_last_modified=get_file_modification_time(test_file_name),
        file_category="video",
    )
    return test_image

def test_dummy():
    assert True

def test_camera_transfer(get_image):
    location = str(Path(__file__).parent / "DCIM/100NIKON")
    input_file_getter = OSFileGetter(location=location, file_extensions={".jpg", ".JPG"}, file_category="image")
    output_file_writer = mock.Mock(spec=OutputFileWriter)

    camera_transfer_operation = CameraTransfer(
        input_file_getter=input_file_getter,
        model_short_names={"COOLPIX S9700": "S9700"},
        output_file_writer=output_file_writer,
        hash_store=HashStore(filename=":memory:"),
    )
    camera_transfer_operation.run()

    assert output_file_writer.write_file.call_count == 1
    assert output_file_writer.write_file.called_once_with('2022-07-27T115409_S9700_1006228.JPG', datetime(2022, 7, 27, 11, 54, 8))

def test_camera_transfer_duplicate(get_image):

    location = str(Path(__file__).parent / "DCIM/100NIKON")

    input_file_getter = OSFileGetter(location=location, file_extensions={".jpg", ".JPG"}, file_category="image")
    output_file_writer = mock.Mock(spec=OutputFileWriter)
    hash_store=HashStore(filename=":memory:")

    camera_transfer_operation = CameraTransfer(
        input_file_getter=input_file_getter,
        model_short_names={"COOLPIX S9700": "S9700"},
        output_file_writer=output_file_writer,
        hash_store=hash_store
    )
    camera_transfer_operation.run()

    # now re-run for the same input file location, and the same hash store instance.
    input_file_getter = OSFileGetter(location=location, file_extensions={".jpg", ".JPG"}, file_category="image")
    camera_transfer_operation = CameraTransfer(
        input_file_getter=input_file_getter,
        model_short_names={"COOLPIX S9700": "S9700"},
        output_file_writer=output_file_writer,
        hash_store=hash_store
    )
    camera_transfer_operation.run()

    assert output_file_writer.write_file.call_count == 1
    assert output_file_writer.write_file.called_once_with('2022-07-27T115409_S9700_1006228.JPG', datetime(2022, 7, 27, 11, 54, 8))


def test_video_transfer(get_video):
    input_file_getter = mock.Mock(spec=InputFileGetter)
    input_file_getter.get_next_file.return_value = [get_video]

    output_file_writer = mock.Mock(spec=OutputFileWriter)

    camera_transfer_operation = CameraTransfer(
        input_file_getter=input_file_getter,
        model_short_names={"COOLPIX S9700": "S9700"},
        output_file_writer=output_file_writer,
        hash_store=HashStore(filename=":memory:"),
    )
    camera_transfer_operation.run()

    assert output_file_writer.write_file.call_count == 1
    assert output_file_writer.write_file.called_once_with('2022-07-27T115409_1006228.MOV', datetime(2022, 7, 27, 11, 54, 8))

def test_video_transfer_duplicate(get_video):
    def side_effect():
        yield(get_video)
        yield(get_video)

    input_file_getter = mock.Mock(spec=InputFileGetter)
    input_file_getter.get_next_file.return_value = [get_video, get_video]
    output_file_writer = mock.Mock(spec=OutputFileWriter)

    camera_transfer_operation = CameraTransfer(
        input_file_getter=input_file_getter,
        model_short_names={"COOLPIX S9700": "S9700"},
        output_file_writer=output_file_writer,
        hash_store=HashStore(filename=":memory:"),
    )
    camera_transfer_operation.run()

    assert output_file_writer.write_file.call_count == 1
    assert output_file_writer.write_file.called_once_with('2022-07-27T115409_1006228.MOV', datetime(2022, 7, 27, 11, 54, 8))
