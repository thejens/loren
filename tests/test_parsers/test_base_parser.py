# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from loren.parsers.base_parser import BaseParser


def test_base_parser() -> None:
    assert BaseParser.parse({"file_contents": "a = 1"}) == {"file_contents": "a = 1"}
