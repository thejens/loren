import pytest
from loren.parsers.base_parser import BaseParser


def test_base_parser_raises():
    with pytest.raises(NotImplementedError):
        BaseParser.parse("")
