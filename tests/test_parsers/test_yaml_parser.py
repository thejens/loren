# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from loren.parsers.base_parser import BaseParser
from loren.parsers.yaml_parser import YamlParser


def test_class() -> None:
    assert issubclass(YamlParser, BaseParser)


def test_yaml_parser() -> None:
    assert YamlParser.parse({"file_contents": "test: a"}) == {"test": "a"}
