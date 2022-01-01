from loren.parsers.base_parser import BaseParser
from loren.parsers.json_parser import JSONParser


def test_class():
    assert issubclass(JSONParser, BaseParser)


def test_json_parser():
    assert JSONParser.parse({"file_contents": '{"a": 1}'}) == {"a": 1}
