import json
from typing import Dict, Any
from .base_parser import BaseParser


class JSONParser(BaseParser):

    @staticmethod
    def parse(file_contents: str) -> Dict[str, Any]:
        return json.loads(file_contents)
