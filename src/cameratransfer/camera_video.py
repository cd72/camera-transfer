
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CameraVideo:
    def __init__(self, video_bytes: bytes, video_basename: str, video_modification_time: datetime) -> None:
        self.video_bytes = video_bytes
        self.video_basename = video_basename
        self.video_modification_time = video_modification_time

    def generate_new_file_name(self) -> str:
        logger.debug(self.video_basename)
        logger.debug(self.video_modification_time)
        video_modification_time_string = self.video_modification_time.strftime("%Y%m%d%H%M%S")
        return f"{video_modification_time_string}_video.mp4"