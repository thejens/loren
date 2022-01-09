# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from loren.parsers.base_parser import BaseParser
from loren.parsers.base64_parser import Base64Parser, URLSafeBase64Parser


def test_class() -> None:
    assert issubclass(Base64Parser, BaseParser)
    assert issubclass(URLSafeBase64Parser, BaseParser)


def test_base64_parser() -> None:
    assert Base64Parser.parse({"file_contents": "abc123/+="}) == {
        "file_contents": "YWJjMTIzLys9"
    }


def test_urlsafe_base64_parser() -> None:
    assert URLSafeBase64Parser.parse({"file_contents": "abc123/+="}) == {
        "file_contents": "YWJjMTIzLys9"
    }
