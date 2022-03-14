# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from pathlib import Path
from loren.utilities.file_reader import LorenFileReader
import pytest

def test_file_reader(tmp_path: Path) -> None:
    with open(f"{tmp_path}/.some_file.yml", "w+", encoding="utf-8") as raw_file:
        raw_file.write("some test text")

    assert LorenFileReader.read(tmp_path.joinpath(".some_file.yml")) == {
        "file_contents": "some test text"
    }


def test_file_reader_empty_file(tmp_path: Path) -> None:
    with open(f"{tmp_path}/some_empty_file.yml", "w+", encoding="utf-8"):
        pass

    assert LorenFileReader.read(tmp_path.joinpath("some_empty_file.yml")) == {
        "file_contents": ""
    }

def test_file_reader_non_existing_file() -> None:
     with pytest.raises(FileNotFoundError):
        LorenFileReader.read(Path("some_non_existing_file.yml"))
