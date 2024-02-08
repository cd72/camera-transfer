from cameratransfer.camera_transfer import CameraTransfer
from cameratransfer.dotenv_config import Settings
from cameratransfer.os_file_getter import OSFileGetter
from cameratransfer.camera_file_getter import CameraFileGetter
from cameratransfer.os_output_file_writer import OSOutputFileWriter
from cameratransfer.hash_store import HashStore
from pathlib import Path
import logging


def set_up_logging(log_level: str) -> None:
    formatter = logging.Formatter(
        "%(module)20s %(asctime)s.%(msecs)03d [%(filename)30s:%(lineno)04d] %(levelname)-8s %(funcName)-30s %(message)s"
        # %(name)s
    )
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(logging.DEBUG)
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(ch)
    print(f"current root logger handlers are {logging.getLogger().handlers}")
    print(__name__)
    root_logger.setLevel(log_level)
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("s3transfer").setLevel(logging.WARNING)


def load_settings_from_dotenv(dotenv_file: Path) -> Settings:
    s = Settings(_env_file="/mnt/d/projects/camera-transfer/tests/test.env")

    import rich

    rich.print(s.model_dump())
    return s


def file_getter(settings: Settings) -> OSFileGetter:
    all_formats = settings.image_formats | settings.video_formats
    return OSFileGetter(location=settings.camera_folder, file_extensions=all_formats)


def camera_file_getter(settings: Settings) -> CameraFileGetter:
    return CameraFileGetter(
        file_getter=file_getter(settings),
        camera_model_short_names=settings.camera_model_short_names,
        image_formats=settings.image_formats,
        video_formats=settings.video_formats,
    )


def get_camera_transfer_operation(settings: Settings) -> CameraTransfer:
    return CameraTransfer(
        camera_file_getter=camera_file_getter(settings),
        output_file_writer=OSOutputFileWriter(
            base_image_location=settings.main_photos_folder,
            base_video_location=settings.main_photos_folder,
            dry_run=settings.dry_run,
        ),
        hash_store=HashStore(filename=settings.sqlite_database),
    )


logger = logging.getLogger(__name__)
logger.info("Running")

camera_model_short_names = {
    "COOLPIX S9700": "S9700",
    "Canon IXUS 115 HS": "IXUS115HS",
    "NIKON Z fc": "ZFC",
    "TFY-LX1": "X8",
}

if __name__ == "__main__":
    load_settings_from_dotenv(Path("/mnt/d/projects/camera-transfer/tests/test.env"))
#     set_up_logging(log_level="DEBUG")
#     camera_transfer_operation = CameraTransfer(
#         camera_file_getter==OSFileGetter(
#             location="/mnt/d/projects/camera-transfer/tests/DCIM", file_extensions={".jpg", ".JPG", ".jpeg", ".JPEG"}
#         ),
#         camera_model_short_names=model_short_names,
#         output_file_writer=OSOutputFileWriter(location="/mnt/d/projects/camera-transfer/tests/DCIM"),
#         hash_store=HashStore(filename=None),
#     )


#     camera_transfer_operation.run()
