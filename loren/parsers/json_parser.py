import json
from typing import Dict, Any
from parsers.base_parser import BaseParser


class JSONParser(BaseParser):

    @staticmethod
    def parse(file_contents: str, **kwargs) -> Dict[str, Any]:
        try:
            file_contents = file_contents.decode("utf-8")
        except (UnicodeDecodeError, AttributeError):
            pass
        return json.loads(file_contents)
