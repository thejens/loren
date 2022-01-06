import base64
from typing import Dict, Any
from loren.parsers.base_parser import BaseParser


class Base64Parser(BaseParser):
    @classmethod
    def parse(cls, data: Dict[str, str], **kwargs) -> Dict[str, Any]:
        try:
            raw_data = data["file_contents"].encode()
        except (UnicodeDecodeError, AttributeError):
            raw_data = data["file_contents"]
        return {"file_contents": base64.b64encode(raw_data).decode("utf-8")}


class URLSafeBase64Parser(BaseParser):
    @classmethod
    def parse(cls, data: Dict[str, str], **kwargs) -> Dict[str, Any]:
        try:
            raw_data = data["file_contents"].encode()
        except (UnicodeDecodeError, AttributeError):
            raw_data = data["file_contents"]
        return {"file_contents": base64.urlsafe_b64encode(raw_data).decode("utf-8")}
