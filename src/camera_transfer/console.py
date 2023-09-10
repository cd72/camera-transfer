import argparse
import logging

from camera_transfer.camera_transfer import CameraTransfer
from camera_transfer.dotenv_config import config

from . import __version__

logger = logging.getLogger(__name__)

log_cli_format = (
    "%(asctime)s.%(msecs)03d [%(filename)20s:%(lineno)04d]"
    + " %(levelname)-8s %(funcName)-30s %(message)s"
)
log_cli_date_format = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(
    level=logging.DEBUG, format=log_cli_format, datefmt=log_cli_date_format
)


def parse_args() -> argparse.Namespace:
    """parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Transfer photos and videos from a camera and organise them in the photos folder."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show what would be transferred without actually doing it.",
    )
    return parser.parse_args()


def main():
    logger.debug("Hello, world!, version: %s", __version__)
    args = parse_args()
    logger.debug(f"args: {args}")
    logger.debug(f"args.dry_run: {args.dry_run}")

    logger.debug(f"config: {config.model_dump}")
    # print(f"Camera folder is {settings.camera_folder}")


    transfer = CameraTransfer(
        camera_folder=config.camera_folder,
        main_photos_folder=config.main_photos_folder,
        sqlite_database=config.sqlite_database,
        dry_run=args.dry_run,
    )


    transfer.transfer_photos()
    # for image in transfer.all_camera_images():
    #     logger.debug(image)
    #     logger.debug(type(image))
    #     for item in image.image_exif.list_all():
    #         if item in ('make', 'model', 'software', 'datetime', 'focal_length', 'f_number', 'exposure_time', 'photographic_sensitivity'):
    #             logger.debug("item %s: %s", item, getattr(image, item)  )
