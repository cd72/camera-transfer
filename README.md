# Camera Transfer
Cross platform app fof processing and organising camera photos and videos.

Flexible to allow additional file getters or writers so enable sources and destinations other than a local filesystem.

An example settings file is as follows
```
CT_CAMERA_FOLDER=/media/cam1
CT_MAIN_PHOTOS_FOLDER=/home/user/Pictures
CT_MAIN_VIDEOS_FOLDER=/home/user/Videos
CT_SQLITE_DATABASE=/home/user/.local/share/camera-transfer/camera-transfer.db
CT_CAMERA_MODEL_SHORT_NAMES='{"COOLPIX S9700": "S9700", "TFY-LX1": "phone"}'
CT_IMAGE_FORMATS='[".jpg", ".jpeg", ".JPG", ".JPEG", ".png", ".PNG"]'
CT_VIDEO_FORMATS='[".mov", ".MOV",  ".mp4", ".MP4"]'
CT_DRY_RUN=False
CT_LOG_LEVEL=INFO
```
