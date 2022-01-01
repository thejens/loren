from typing import Dict, Any
from loren.parsers.base_parser import BaseParser


class PyParser(BaseParser):
    @staticmethod
    def parse(data: Dict[str, str], **kwargs) -> Dict[str, Any]:
        try:
            file_contents = data["file_contents"].decode("utf-8")
        except AttributeError:
            file_contents = data["file_contents"]
        local_vars: Dict[str, Any] = {}
        global_vars: Dict[str, Any] = {}
        exec(file_contents, global_vars, local_vars)
        local_vars.update(
            {key: value for key, value in global_vars.items() if key[0] != "_"}
        )
        return local_vars
