from loren.parsers.base_parser import BaseParser
from loren.parsers.yaml_parser import YamlParser


def test_class():
    assert issubclass(YamlParser, BaseParser)


def test_csv_parser():
    assert YamlParser.parse("test: a") == {"test": "a"}
