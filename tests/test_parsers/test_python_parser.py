from omniparse.parsers.base_parser import BaseParser
from omniparse.parsers.python_parser import PyParser


def test_class():
    assert issubclass(PyParser, BaseParser)


def test_csv_parser():
    assert PyParser.parse('a = 1') == {"py_vars": {"a": 1}}
