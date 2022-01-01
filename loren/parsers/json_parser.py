import json
from typing import Dict, Any
from loren.parsers.base_parser import BaseParser


class JSONParser(BaseParser):
    
    @classmethod
    def parse(cls, data: Dict[str, str], **kwargs) -> Dict[str, Any]:
        try:
            file_contents = data["file_contents"].decode("utf-8")
        except AttributeError:
            file_contents = data["file_contents"]
        return json.loads(file_contents)
