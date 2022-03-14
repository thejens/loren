# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=too-few-public-methods
from typing import Dict, Any
from pathlib import Path
import os
import re
import jinja2
from loren.parsers.base_parser import BaseParser

template_functions = {"list": list, "dict": dict, "len": len, "range": range}


class Jinja2Parser(BaseParser):
    @classmethod
    def _parse(
        cls,
        data: Dict[str, str],
        file_path: Path = None,
        root_path: Path = None,
        additional_args: Dict = None,
    ) -> Dict[str, str]:
        additional_args = additional_args or {}
        template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(root_path))
        )
        template = template_env.from_string(data["file_contents"])
        return {
            "file_contents": template.render(
                env=dict(os.environ), re=re, **template_functions, **additional_args
            )
        }
