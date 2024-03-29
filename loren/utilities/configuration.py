# pylint: disable=missing-class-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import os
from importlib import import_module
from functools import lru_cache
from typing import Type
from pathlib import Path
import yaml
import pathspec
from loren.parsers.base_parser import BaseParser


CONFIG_FILE_NAME = ".loren.yml"
DEFAULT_CONFIG: dict = {
    "file_handlers": {
        "yaml": "loren.parsers.yaml_parser.YamlParser",
        "yml": "loren.parsers.yaml_parser.YamlParser",
        "json": "loren.parsers.json_parser.JSONParser",
        "py": "loren.parsers.python_parser.PyParser",
        "csv": "loren.parsers.csv_parser.CSVParser",
        "tsv": "loren.parsers.csv_parser.TSVParser",
        "j2": "loren.parsers.jinja2_parser.Jinja2Parser",
        "jinja2": "loren.parsers.jinja2_parser.Jinja2Parser",
        "jpg": "loren.parsers.base64_parser.Base64Parser",
        "png": "loren.parsers.base64_parser.Base64Parser",
        "gif": "loren.parsers.base64_parser.Base64Parser",
        "*": "loren.parsers.base_parser.BaseParser",
    },
    "ignore": [
        ".loren.yml",
        ".DS_Store",
        "_*",
        ".*",
    ],
}


class LorenConfiguration:
    @staticmethod
    def create_default_configuration(path: Path) -> None:
        os.makedirs(path, exist_ok=True)
        with open(path.joinpath(CONFIG_FILE_NAME), "w", encoding="utf-8") as file:
            yaml.dump(DEFAULT_CONFIG, file)

    def __init__(self, path: Path = Path(".")):
        self.file_handlers = DEFAULT_CONFIG["file_handlers"].copy()
        self.ignore = DEFAULT_CONFIG["ignore"].copy()

        try:
            with open(path.joinpath(CONFIG_FILE_NAME), "r", encoding="utf-8") as file:
                config = yaml.safe_load(file)
                if "file_handlers" in config:
                    self.file_handlers = config["file_handlers"].copy()
                if "ignore" in config:
                    self.ignore = config["ignore"].copy()

        except (FileNotFoundError, NotADirectoryError):
            pass

        self.ignore_paths = pathspec.PathSpec.from_lines("gitwildmatch", self.ignore)
        self.base_path = path

    @lru_cache()
    def get_parser_class(self, file_extension: str) -> Type[BaseParser]:
        parser_class_path = self.file_handlers.get(
            file_extension, self.file_handlers["*"]
        )
        return getattr(
            import_module(".".join(parser_class_path.split(".")[:-1])),
            parser_class_path.split(".")[-1],
        )

    def is_ignored_file(self, item: Path) -> bool:
        return self.ignore_paths.match_file(
            str(item)[len(str(self.base_path)) + 1 :] + ("/" if item.is_dir() else "")
        )
