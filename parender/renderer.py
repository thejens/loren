import jinja2
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
    render_path: str,
    configurations: dict
) -> None:
    for result in _read_template(template_path).render(
        **configurations,
        **template_functions,
        env=dict(environ)
    ).split("=>")[1:]:
        file_name, file_contents = result.split('\n', 1)
        result_path = join(render_path, file_name)
        result_folder = '/'.join(result_path.split("/")[:-1])
        if not isdir(result_folder):
            makedirs(result_folder)
        with open(result_path, "w+") as f:
            f.write(file_contents)
