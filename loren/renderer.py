import jinja2
import re
from os import makedirs, environ
from os.path import join, isdir


template_functions = {
    "list": list,
    "dict": dict,
    "len": len,
    "range": range
}


def _read_template(template_path: str) -> jinja2.Template:
    with open(template_path, "r") as template_file:
        return jinja2.Template(template_file.read())


def render(
    template_path: str,
    output_path: str,
    configurations: dict
) -> None:
    files = re.split(
        r"^=>",
        _read_template(template_path).render(
            **configurations,
            **template_functions,
            env=dict(environ),
            re=re
        ),
        0,
        re.MULTILINE
    )
    if len(files) == 1:
        with open(output_path, "wb") as f:
            f.write(files[0].encode('utf-8'))
    else:
        for result in files[1:]:
            file_name, file_contents = result.split('\n', 1)
            result_path = join(output_path, file_name)
            result_folder = '/'.join(result_path.split("/")[:-1])
            if not isdir(result_folder):
                makedirs(result_folder)
            with open(result_path, "wb") as f:
                f.write(file_contents.encode('utf-8'))
