from loren.parsers.base_parser import BaseParser
from loren.parsers.json_parser import JSONParser


def test_class():
    assert issubclass(JSONParser, BaseParser)


def test_csv_parser():
    assert JSONParser.parse('{"a": 1}') == {"a": 1}
