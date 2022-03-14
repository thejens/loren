# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=too-few-public-methods
import json
from typing import Dict, Any
from pathlib import Path
from loren.parsers.base_parser import BaseParser


class JSONParser(BaseParser):
    @classmethod
    def _parse(
        cls,
        data: Dict[str, str],
        file_path: Path = None,
        root_path: Path = None,
        additional_args: Dict = None,
    ) -> Dict[str, Any]:
        return json.loads(data["file_contents"])
