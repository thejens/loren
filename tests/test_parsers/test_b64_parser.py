from loren.parsers.base_parser import BaseParser
from loren.parsers.base64_parser import Base64Parser, URLSafeBase64Parser


def test_class():
    assert issubclass(Base64Parser, BaseParser)
    assert issubclass(URLSafeBase64Parser, BaseParser)


def test_base64_parser():
    assert Base64Parser.parse({"file_contents": "abc123/+="}) == {
        "file_contents": "YWJjMTIzLys9"
    }
    assert Base64Parser.parse({"file_contents": "abc123/+="}) == Base64Parser.parse(
        {"file_contents": b"abc123/+="}
    )


def test_urlsafe_base64_parser():
    assert URLSafeBase64Parser.parse({"file_contents": "abc123/+="}) == {
        "file_contents": "YWJjMTIzLys9"
    }
    assert URLSafeBase64Parser.parse(
        {"file_contents": "abc123/+="}
    ) == Base64Parser.parse({"file_contents": b"abc123/+="})
