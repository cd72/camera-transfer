import argparse
import logging
from pathlib import Path

from cameratransfer.camera_file_getter import CameraFileGetter
from cameratransfer.camera_transfer import CameraTransfer
from cameratransfer.dotenv_config import Settings
from cameratransfer.hash_store import HashStore
from cameratransfer.os_file_getter import OSFileGetter
from cameratransfer.os_output_file_writer import OSOutputFileWriter


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

def load_settings_from_dotenv(dotenv_file: Path) -> Settings:
    s = Settings(_env_file=dotenv_file)

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


def main() -> None:
    logger = logging.getLogger(__name__)
    logger.info("Running")

    args = parse_args()


    settings = load_settings_from_dotenv(Path(__file__).parent / "settings.env")
    set_up_logging(settings.log_level)
    # "/mnt/d/projects/camera-transfer/settings.env"
    if args.dry_run:
        settings.dry_run = True
    camera_transfer_operation = get_camera_transfer_operation(settings)
    camera_transfer_operation.run()

if __name__ == "__main__":
    main()
