# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from loren.parsers.base_parser import BaseParser
from loren.parsers.python_parser import PyParser


def test_class() -> None:
    assert issubclass(PyParser, BaseParser)


def test_csv_parser() -> None:
    assert PyParser.parse({"file_contents": "a = 1"}) == {"a": 1}
