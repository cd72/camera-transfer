from pathlib import Path
import pytest
from datetime import datetime

# @pytest.fixture()
# def get_file_text():
#     def _(file_path: str):
#         return (Path(__file__).parent / file_path).read_text()

#     return _


@pytest.fixture()
def get_file_bytes():
    def _(file_path: str) -> bytes:
        return (Path(__file__).parent / file_path).read_bytes()

    return _


@pytest.fixture()
def get_file_modification_time():
    def _(file_path: str) -> datetime:
        return datetime.fromtimestamp(
            (Path(__file__).parent / file_path).stat().st_mtime
        )

    return _
