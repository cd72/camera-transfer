from cameratransfer.camera_transfer import CameraTransfer
from cameratransfer.dotenv_config import Settings
from cameratransfer.os_file_getter import OSFileGetter
from cameratransfer.os_output_file_writer import OSOutputFileWriter
from cameratransfer.hash_store import HashStore
import logging

def set_up_logging(log_level: str):
    formatter = logging.Formatter(
        "%(module)20s %(asctime)s.%(msecs)03d [%(filename)30s:%(lineno)04d] %(levelname)-8s %(funcName)-30s %(message)s"
        #%(name)s
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



logger = logging.getLogger(__name__)
logger.info("Running")

model_short_names ={
        "COOLPIX S9700": "S9700",
        "Canon IXUS 115 HS": "IXUS115HS",
        "NIKON Z fc": "ZFC",
        "TFY-LX1": "X8",
    }

# if __name__ == "__main__":
#     set_up_logging(log_level="DEBUG")
#     camera_transfer_operation = CameraTransfer(
#         camera_file_getter==OSFileGetter(
#             location="/mnt/d/projects/camera-transfer/tests/DCIM", file_extensions={".jpg", ".JPG", ".jpeg", ".JPEG"}
#         ),
#         model_short_names=model_short_names,
#         output_file_writer=OSOutputFileWriter(location="/mnt/d/projects/camera-transfer/tests/DCIM"),
#         hash_store=HashStore(filename=":memory:"),
#     )


#     camera_transfer_operation.run()
