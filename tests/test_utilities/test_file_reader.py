# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from pathlib import Path
from loren.utilities.file_reader import LorenFileReader


def test_file_reader(tmp_path: Path) -> None:
    with open(f"{tmp_path}/.some_file.yml", "w+", encoding="utf-8") as raw_file:
        raw_file.write("some test text")

    assert LorenFileReader.read(tmp_path.joinpath(".some_file.yml")) == {
        "file_contents": "some test text"
    }
