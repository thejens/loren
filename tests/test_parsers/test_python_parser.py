from loren.parsers.base_parser import BaseParser
from loren.parsers.python_parser import PyParser


def test_class():
    assert issubclass(PyParser, BaseParser)


def test_csv_parser():
    assert PyParser.parse("a = 1") == {"a": 1}
