from typing import Dict, Any
from parsers.base_parser import BaseParser


class PyParser(BaseParser):

    @staticmethod
    def parse(file_contents: str, **kwargs) -> Dict[str, Any]:
        try:
            file_contents = file_contents.decode("utf-8")
        except (UnicodeDecodeError, AttributeError):
            pass
        local_vars: Dict[str, Any] = {}
        global_vars: Dict[str, Any] = {}
        exec(file_contents, global_vars, local_vars)
        local_vars.update({key: value for key, value in global_vars.items() if key[0] != "_"})
        return local_vars
