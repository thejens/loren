from typing import Dict, Any
from loren.parsers.base_parser import BaseParser


class TextParser(BaseParser):
    @staticmethod
    def parse(data: Dict[str, str], **kwargs) -> Dict[str, Any]:
        try:
            file_contents = data["file_contents"].decode("utf-8")
        except AttributeError:
            file_contents = data["file_contents"]
        return {"file_contents": file_contents}
