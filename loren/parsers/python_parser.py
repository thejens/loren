from typing import Dict, Any
from .base_parser import BaseParser


class PyParser(BaseParser):

    @staticmethod
    def parse(file_contents: str) -> Dict[str, Any]:
        local_vars: Dict[str, Any] = {}
        exec(file_contents, {}, local_vars)
        return local_vars
