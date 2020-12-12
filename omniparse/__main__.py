import argparse
import warnings
import json
import yaml
import functools
import importlib
import pathspec

try:
    import jsonschema
except ImportError:
    warnings.warn("jsonschema not installed, not able to validate config")

from pprint import pprint
from os import listdir
from os.path import isfile, join

from .parsers.base_parser import BaseParser
from .file_loaders.base_loader import BaseLoader

from typing import Union, Dict, Type, Any, List, Callable

DEFAULT_PARSERS: Dict[str, str] = {
    "yaml": "omniparse.parsers.yaml_parser.YamlParser",
    "yml": "omniparse.parsers.yaml_parser.YamlParser",
    "json": "omniparse.parsers.json_parser.JSONParser",
    "py": "omniparse.parsers.python_parser.PyParser",
    "csv": "omniparse.parsers.csv_parser.CSVParser",
    "tsv": "omniparse.parsers.csv_parser.TSVParser",
    "*": "omniparse.parsers.text_parser.TextParser"
}

DEFAULT_LOADERS: Dict[str, str] = {
    "j2": "omniparse.file_loaders.jinja2_loader.Jinja2Loader",
    "jinja2": "omniparse.file_loaders.jinja2_loader.Jinja2Loader",
    "jpg": "omniparse.file_loaders.base64_loader.URLSafeBase64Loader",
    "png": "omniparse.file_loaders.base64_loader.URLSafeBase64Loader",
    "*": "omniparse.file_loaders.text_loader.TextLoader"
}


DEFAULT_IGNORED_PATTERNS: List[str] = [
    ".*",
    "_*"
]


@functools.lru_cache()
def get_config(root_dir) -> Dict[str, Any]:
    print(root_dir)
    try:
        with open(join(root_dir, ".omniparse.yaml"), "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {}


@functools.lru_cache()
def get_parsers(base_path) -> Dict[str, str]:
    conf = get_config(base_path)
    return conf.get("parsers", DEFAULT_PARSERS)


@functools.lru_cache()
def get_loaders(base_path) -> Dict[str, str]:
    conf = get_config(base_path)
    return conf.get("loaders", DEFAULT_LOADERS)


@functools.lru_cache()
def get_loader_class(class_ref) -> Type[BaseLoader]:
    print(".".join(class_ref.split(".")[:-1]))
    print(class_ref.split(".")[-1])
    return getattr(
        importlib.import_module(".".join(class_ref.split(".")[:-1])),
        class_ref.split(".")[-1]
    )


@functools.lru_cache()
def get_parser_class(class_ref) -> Type[BaseParser]:
    return getattr(
        importlib.import_module(".".join(class_ref.split(".")[:-1])),
        class_ref.split(".")[-1]
    )


@functools.lru_cache()
def get_ignore(base_path) -> Callable[[str], bool]:
    try:
        with open(join(base_path, ".omniparseignore"), "r") as f:
            spec = pathspec.PathSpec.from_lines('gitwildmatch', f)
    except FileNotFoundError:
        spec = pathspec.PathSpec.from_lines(
            'gitwildmatch',
            DEFAULT_IGNORED_PATTERNS
        )
    return lambda file_name: file_name in set(spec.match_tree(base_path))


def parse(
    path: str,
    base_path: Union[None, str] = None,
    **kwargs
) -> Dict:
    if not base_path:
        base_path = path
    parsers = get_parsers(base_path)
    loaders = get_loaders(base_path)
    ignore_func = get_ignore(base_path)

    configs: Dict[str, Any] = {}
    for item in listdir(path):
        item_path = join(path, item)
        extensions = item.split(".")
        key = extensions[0]
        sub_path = item_path[len(base_path):].strip("/")

        if isfile(item_path):
            if ignore_func(sub_path):
                print(f"Ignoring: {sub_path}")
                continue
            else:
                print(f"Keeping: {sub_path}")

            if extensions[-1] in loaders:
                loader_extension = extensions[-1]
                extensions = extensions[:-1]
            else:
                loader_extension = "*"

            if extensions[-1] in parsers:
                parser_extension = extensions[-1]
            else:
                parser_extension = "*"

            loader = get_loader_class(loaders[loader_extension])
            parser = get_parser_class(parsers[parser_extension])

            raw_contents = loader.load(item_path, base_path, **kwargs)
            parsed_contents = parser.parse(raw_contents)

            child = parsed_contents
            child["_path"] = item_path
        else:
            if ignore_func(sub_path):
                print(f"Ignoring: {sub_path}")
                continue
            else:
                print(f"Keeping: {sub_path}")

            child = parse(
                item_path,
                base_path,
                **kwargs
            )
        if key in configs:
            warnings.warn(
                f"Merging contents for key {key} " +
                f"due to multiple files/folders with same prefix in {path}"
            )
            configs[key].update(child)
        else:
            configs[key] = child
    return configs


def validate(configurations: dict, schema_path: str) -> None:
    with open(schema_path, "r") as schema:
        jsonschema.validate(configurations, json.load(schema))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Transform a file-tree into a configuration blob'
    )
    parser.add_argument('path', type=str)
    parser.add_argument('--output-file', type=str, default="")
    parser.add_argument('--schema-file', type=str, default=False)
    args = parser.parse_args()

    configurations = parse(args.path)
    if args.schema_file:
        validate(configurations, args.schema_file)

    if not args.output_file:
        pprint(configurations)
    else:
        with open(args.output_file, "w+") as f:
            f.write(json.dumps(configurations))
