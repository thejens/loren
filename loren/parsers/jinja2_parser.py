from typing import Dict, Any
from parsers.base_parser import BaseParser
import jinja2
import os
import re

template_functions = {
    "list": list,
    "dict": dict,
    "len": len,
    "range": range
}

class Jinja2Parser(BaseParser):
    
    @classmethod
    def parse(cls, file_contents: str, root_path, **kwargs) -> Dict[str, str]:
        templateEnv = jinja2.Environment(loader=jinja2.FileSystemLoader(root_path))
        try:
            file_contents = file_contents.decode("utf-8")
        except (UnicodeDecodeError, AttributeError):
            pass
        
        template = templateEnv.from_string(file_contents)
        return {
            "file_contents": template.render(env=os.environ, re=re, **template_functions)
        }
