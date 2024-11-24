import argparse
import logging
from pathlib import Path
import rich

import platformdirs


from camera_transfer.camera_file_getter import CameraFileGetter
from camera_transfer.camera_transfer import CameraTransfer
from camera_transfer.camera_settings import CameraSettings
from camera_transfer.hash_store import HashStore
from camera_transfer.os_file_getter import OSFileGetter
from camera_transfer.os_output_file_writer import OSOutputFileWriter


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
    root_logger.setLevel(log_level)

    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("s3transfer").setLevel(logging.WARNING)

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Transfer photos and videos from a camera and organise them in the photos folder."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be transferred without actually doing it.",
    )
    return parser.parse_args()

def create_settings_file(settings_file: Path) -> None:
    print(f"Creating settings file {settings_file}")
    settings_file.parent.mkdir(parents=True, exist_ok=True)
    settings_file.write_text(f"""
CT_CAMERA_FOLDER=.
CT_MAIN_PHOTOS_FOLDER={platformdirs.user_pictures_path()}
CT_MAIN_VIDEOS_FOLDER={platformdirs.user_videos_path()}
CT_SQLITE_DATABASE={platformdirs.user_data_dir('camera-transfer')}/camera-transfer.db
CT_CAMERA_MODEL_SHORT_NAMES='{{"COOLPIX S9700": "S9700", "TFY-LX1": "chris-phone"}}'
CT_IMAGE_FORMATS='[".jpg", ".jpeg", ".JPG", ".JPEG", ".png", ".PNG"]'
CT_VIDEO_FORMATS='[".mov", ".MOV",  ".mp4", ".MP4"]'
CT_DRY_RUN=False
CT_LOG_LEVEL=INFO
""")

def load_settings_from_file(settings_file: Path) -> CameraSettings:
    if not settings_file.exists():
       print(f"The settings file {settings_file} does not exist.")
       create_settings_file(settings_file)

    print(f"Loading settings from {settings_file}")
    s = CameraSettings(_env_file=settings_file)

    rich.print(s.model_dump())
    return s


def file_getter(settings: CameraSettings) -> OSFileGetter:
    all_formats = settings.image_formats | settings.video_formats
    return OSFileGetter(location=settings.camera_folder, file_extensions=all_formats)


def camera_file_getter(settings: CameraSettings) -> CameraFileGetter:
    return CameraFileGetter(
        file_getter=file_getter(settings),
        camera_model_short_names=settings.camera_model_short_names,
        image_formats=settings.image_formats,
        video_formats=settings.video_formats,
    )


def get_camera_transfer_operation(settings: CameraSettings) -> CameraTransfer:
    return CameraTransfer(
        camera_file_getter=camera_file_getter(settings),
        output_file_writer=OSOutputFileWriter(
            base_image_location=settings.main_photos_folder,
            base_video_location=settings.main_photos_folder,
            dry_run=settings.dry_run,
        ),
        hash_store=HashStore(filename=settings.sqlite_database),
    )


def main() -> None:
    logger = logging.getLogger(__name__)

    args = parse_args()

    settings_file = Path(platformdirs.user_config_dir("camera-transfer")) / "settings.env"
    settings = load_settings_from_file(settings_file=settings_file)
    set_up_logging(settings.log_level)
    if args.dry_run:
        logger.info("Dry run mode")
        settings.dry_run = True
    camera_transfer_operation = get_camera_transfer_operation(settings)
    camera_transfer_operation.run()

if __name__ == "__main__":
    main()
