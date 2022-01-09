# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import re
from pathlib import Path
from os import makedirs, environ
from os.path import dirname
from typing import List, Union, Tuple, Iterator
import jinja2
from jinja2 import Undefined, StrictUndefined

template_functions = {"list": list, "dict": dict, "len": len, "range": range}


def _read_template(template_path: Path, strict: bool) -> jinja2.Template:
    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(dirname(template_path)),
        undefined=StrictUndefined if strict else Undefined,
    )
    with open(template_path, "r", encoding="utf-8") as template_file:
        return template_env.from_string(
            template_file.read(),
        )


def _get_output_files(rendered_template: str) -> Iterator[Tuple[Path, str]]:
    files = re.split(
        r"^=>",
        rendered_template,
        0,
        re.MULTILINE,
    )
    for file in files:
        if file:
            (file_name, file_contents) = file.split("\n", 1)
            yield Path(file_name.strip()), file_contents


def render(
    template_path: Union[str, List[str]],
    configurations: dict,
    output_path: Union[str, Path] = Path(""),
    strict: bool = False,
    dry_run: bool = False,
) -> None:
    if isinstance(template_path, (Path, str)):
        template_path = [template_path]

    template_paths = [Path(path) for path in template_path]

    if isinstance(output_path, str):
        output_path = Path(output_path)

    for path in template_paths:
        rendered_template = _read_template(path, strict).render(
            **configurations, **template_functions, env=dict(environ), re=re
        )
        if not rendered_template.startswith("=>"):
            if re.match(r".+\..+", output_path.name):
                default_output_file_name = output_path.name
            else:
                default_output_file_name = re.sub(r"(\.j2|\.jinja2)$", "", path.name)
            rendered_template = f"=>{default_output_file_name}\n" + rendered_template

        for (file_path, file_contents) in _get_output_files(rendered_template):
            if re.match(r".+\..+", output_path.name):
                output_path = output_path.parent

            file_path = Path(output_path, file_path)
            if dry_run:
                print(
                    f"{'-'*100}\nOutput file: {file_path}\n"
                    + f"First 100 chars from content:\n {file_contents[:100]}"
                )
            makedirs(file_path.parent, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(file_contents)
