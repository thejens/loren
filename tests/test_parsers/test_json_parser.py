# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from loren.parsers.base_parser import BaseParser
from loren.parsers.json_parser import JSONParser


def test_class() -> None:
    assert issubclass(JSONParser, BaseParser)


def test_json_parser() -> None:
    assert JSONParser.parse({"file_contents": '{"a": 1}'}) == {"a": 1}
