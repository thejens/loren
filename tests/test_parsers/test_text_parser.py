from omniparse.parsers.base_parser import BaseParser
from omniparse.parsers.text_parser import TextParser


def test_class():
    assert issubclass(TextParser, BaseParser)


def test_csv_parser():
    assert TextParser.parse('a = 1') == {"file_contents": 'a = 1'}
