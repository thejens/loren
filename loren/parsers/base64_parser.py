# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=too-few-public-methods
import base64
from typing import Dict
from pathlib import Path
from loren.parsers.base_parser import BaseParser


class Base64Parser(BaseParser):
    @classmethod
    def _parse(
        cls,
        data: Dict[str, str],
        file_path: Path = None,
        root_path: Path = None,
        additional_args: Dict = None,
    ) -> Dict[str, str]:
        return {
            "file_contents": base64.b64encode(
                data["file_contents"].encode("utf-8")
            ).decode("utf-8")
        }


class URLSafeBase64Parser(BaseParser):
    @classmethod
    def _parse(
        cls,
        data: Dict[str, str],
        file_path: Path = None,
        root_path: Path = None,
        additional_args: Dict = None,
    ) -> Dict[str, str]:
        return {
            "file_contents": base64.urlsafe_b64encode(
                data["file_contents"].encode("utf-8")
            ).decode("utf-8")
        }
