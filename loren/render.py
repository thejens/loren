import jinja2
import re
import codecs
from jinja2 import Undefined, StrictUndefined
from os import makedirs, environ
from os.path import join, isdir


template_functions = {"list": list, "dict": dict, "len": len, "range": range}


def _read_template(template_path: str, strict: bool) -> jinja2.Template:
    with open(template_path, "r") as template_file:
        return jinja2.Template(
            template_file.read(), undefined=StrictUndefined if strict else Undefined
        )


def render(
    template_path: str,
    output_path: str,
    configurations: dict,
    strict: bool = False,
    dry_run: bool = False,
) -> None:
    files = re.split(
        r"^=>",
        _read_template(template_path, strict).render(
            **configurations, **template_functions, env=dict(environ), re=re
        ),
        0,
        re.MULTILINE,
    )
    if dry_run:
        print("Dry run successful")
        return

    if len(files) == 1:
        with codecs.open(output_path, "w", "utf-8") as f:
            f.write(str(files[0]))
    else:
        for result in files[1:]:
            file_name, file_contents = result.split("\n", 1)
            result_path = join(output_path, file_name)
            result_folder = "/".join(result_path.split("/")[:-1])
            if not isdir(result_folder):
                makedirs(result_folder)
            with codecs.open(result_path, "w", "utf-8") as f:
                f.write(str(file_contents))
