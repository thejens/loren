import jinja2
import os
from .base_loader import BaseLoader

template_functions = {
    "list": list,
    "dict": dict,
    "len": len,
    "range": range
}


class Jinja2Loader(BaseLoader):
    @staticmethod
    def load(file_path, root_path, **kwargs) -> str:
        template_path = file_path[len(root_path):]
        loader = jinja2.FileSystemLoader(root_path)
        templateEnv = jinja2.Environment(loader=loader)
        template = templateEnv.get_template(template_path)
        return template.render(env=os.environ, **template_functions, **kwargs)
