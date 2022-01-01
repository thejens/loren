from loren.parsers.base_parser import BaseParser
from loren.parsers.yaml_parser import YamlParser


def test_class():
    assert issubclass(YamlParser, BaseParser)


def test_yaml_parser():
    assert YamlParser.parse({'file_contents': "test: a"}) == {"test": "a"}
