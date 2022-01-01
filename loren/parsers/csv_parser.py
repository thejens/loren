import csv
from typing import Dict, Any
from loren.parsers.base_parser import BaseParser


class CSVParser(BaseParser):
    sep = ","

    @classmethod
    def _split_row(cls, row):
        return row.split(cls.sep)

    @classmethod
    def parse(cls, data: Dict[str, str], **kwargs) -> Dict[str, Any]:
        try:
            file_contents = data["file_contents"].decode("utf-8")
        except AttributeError:
            file_contents = data["file_contents"]
        return {
            "rows": list(csv.DictReader(file_contents.splitlines(), delimiter=cls.sep))
        }


class TSVParser(CSVParser):
    sep = "\t"
