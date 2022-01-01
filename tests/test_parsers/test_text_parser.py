from loren.parsers.base_parser import BaseParser
from loren.parsers.text_parser import TextParser


def test_class():
    assert issubclass(TextParser, BaseParser)


def test_csv_parser():
    assert TextParser.parse({"file_contents": "a = 1".encode("utf-8")}) == {
        "file_contents": "a = 1"
    }
