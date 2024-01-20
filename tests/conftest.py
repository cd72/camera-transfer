from pathlib import Path
import pytest

# @pytest.fixture()
# def get_file_text():
#     def _(file_path: str):
#         return (Path(__file__).parent / file_path).read_text()

#     return _


@pytest.fixture()
def get_file_bytes():
    def _(file_path: str):
        return (Path(__file__).parent / file_path).read_bytes()

    return _