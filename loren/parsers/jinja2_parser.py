from typing import Dict, Any
from loren.parsers.base_parser import BaseParser
import jinja2
import os
import re

template_functions = {"list": list, "dict": dict, "len": len, "range": range}


class Jinja2Parser(BaseParser):
    @classmethod
    def parse(
        cls, data: Dict[str, str], root_path, additional_args, **kwargs
    ) -> Dict[str, str]:
        templateEnv = jinja2.Environment(loader=jinja2.FileSystemLoader(root_path))
        try:
            file_contents = data["file_contents"].decode("utf-8")
        except AttributeError:
            file_contents = data["file_contents"]

        template = templateEnv.from_string(file_contents)
        return {
            "file_contents": template.render(
                env=dict(os.environ), re=re, **template_functions, **additional_args
            )
        }
