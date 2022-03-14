# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=too-few-public-methods
from typing import Dict, Any
from pathlib import Path
from loren.parsers.base_parser import BaseParser


class PyParser(BaseParser):
    @classmethod
    def _parse(
        cls,
        data: Dict[str, str],
        file_path: Path = None,
        root_path: Path = None,
        additional_args: Dict = None,
    ) -> Dict[str, Any]:
        local_vars: Dict[str, Any] = {}
        global_vars: Dict[str, Any] = {}
        exec(  # pylint: disable=exec-used
            data["file_contents"], global_vars, local_vars
        )
        local_vars.update(
            {key: value for key, value in global_vars.items() if key[0] != "_"}
        )
        return local_vars
