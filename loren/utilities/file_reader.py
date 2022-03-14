# pylint: disable=missing-class-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from typing import Dict
from pathlib import Path


class LorenFileReader:
    @staticmethod
    def read(file_path: Path) -> Dict[str, str]:
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                return {"file_contents": file.read() or ""}
            except Exception as exception:
                print(f"Exception raised when opening {file_path}")
                raise exception
