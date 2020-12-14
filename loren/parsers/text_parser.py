from typing import Dict, Any
from .base_parser import BaseParser


class TextParser(BaseParser):

    @staticmethod
    def parse(file_contents: str) -> Dict[str, Any]:
        return {"file_contents": file_contents}
