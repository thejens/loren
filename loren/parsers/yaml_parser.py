# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=too-few-public-methods
from typing import Dict, Any
from pathlib import Path
import yaml
from loren.parsers.base_parser import BaseParser


class YamlParser(BaseParser):
    @classmethod
    def _parse(
        cls,
        data: Dict[str, str],
        file_path: Path = None,
        root_path: Path = None,
        additional_args: Dict = None,
    ) -> Dict[str, Any]:
        return yaml.safe_load(data["file_contents"])
