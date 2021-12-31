import csv
from typing import Dict, Any
from parsers.base_parser import BaseParser


class CSVParser(BaseParser):
    sep = ","

    @classmethod
    def _split_row(cls, row):
        return row.split(cls.sep)

    @classmethod
    def parse(cls, file_contents: str, **kwargs) -> Dict[str, Any]:
        try:
            file_contents = file_contents.decode("utf-8")
        except (UnicodeDecodeError, AttributeError):
            pass
        return {"rows": list(
            csv.DictReader(file_contents.splitlines(), delimiter=cls.sep)
        )}


class TSVParser(CSVParser):
    sep = "\t"
