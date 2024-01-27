from cameratransfer.camera_file import CameraFile
from cameratransfer.camera_image import CameraImage
from cameratransfer.camera_video import CameraVideo
from typing import Protocol, Iterator
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class InputFileGetter(Protocol):
    def get_next_file(self) -> Iterator[CameraFile]:
        ...

class OutputFileWriter(Protocol):
    def write_file(self, file_name: str, file_last_modified: datetime) -> None:
        ...

class HashStore(Protocol):
    def __setitem__(self, hash: bytes, file_item: str) -> None:
        ...

    def __contains__(self, hash:bytes) -> bool:
        ...


class CameraTransfer:
    def __init__(self, input_file_getter: InputFileGetter, model_short_names, output_file_writer: OutputFileWriter, hash_store: HashStore) -> None:
        self.input_file_getter = input_file_getter
        self.output_file_writer = output_file_writer
        self.model_short_names = model_short_names
        self.hash_store = hash_store

    def run(self) -> None:
        logger.debug("Starting Camera Transfer")
        for file_to_process in  self.input_file_getter.get_next_file():
            logger.debug("Processing input file %s", file_to_process.file_name)


            if file_to_process.file_category == "image":
                logger.debug(f"file_to_process.file_name: {file_to_process.file_name}")
                camera_image = CameraImage(
                    image_bytes=file_to_process.file_content,
                    image_basename=file_to_process.file_name,
                    model_short_names=self.model_short_names,
                )

                if camera_image.image_hash in self.hash_store:
                    logger.debug("Skipping duplicate photo")
                    continue

                new_file_name = camera_image.generate_new_file_name()
                new_last_modified = file_to_process.file_last_modified
                logger.debug(new_file_name)
                self.output_file_writer.write_file(new_file_name, new_last_modified)
                self.hash_store[camera_image.image_hash] = new_file_name

            if file_to_process.file_category == "video":
                camera_video = CameraVideo(
                    video_bytes=file_to_process.file_content,
                    video_basename=file_to_process.file_name,
                    video_modification_time=file_to_process.file_last_modified
                )
                if camera_video.video_hash in self.hash_store:
                    logger.debug("Skipping duplicate video")
                    continue
            
                new_file_name = camera_video.generate_new_file_name()
                new_last_modified = file_to_process.file_last_modified
                logger.debug(new_file_name)
                self.output_file_writer.write_file(new_file_name, new_last_modified)
                self.hash_store[camera_video.video_hash] = new_file_name



            



            


