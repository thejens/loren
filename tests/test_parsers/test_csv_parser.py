# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from loren.parsers.base_parser import BaseParser
from loren.parsers.csv_parser import CSVParser, TSVParser

CSV_DATA = """a,b,c\n1,2,3\n4,5,6\na,"b,c",d"""


def test_class() -> None:
    assert issubclass(CSVParser, BaseParser)
    assert issubclass(TSVParser, BaseParser)


def test_csv_parser() -> None:
    assert CSVParser.parse({"file_contents": CSV_DATA}) == {
        "rows": [
            {"a": "1", "b": "2", "c": "3"},
            {"a": "4", "b": "5", "c": "6"},
            {"a": "a", "b": "b,c", "c": "d"},
        ]
    }


def test_tsv_parser() -> None:
    assert TSVParser.parse({"file_contents": CSV_DATA.replace(",", "\t")}) == {
        "rows": [
            {"a": "1", "b": "2", "c": "3"},
            {"a": "4", "b": "5", "c": "6"},
            {"a": "a", "b": "b\tc", "c": "d"},
        ]
    }
