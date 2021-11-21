
import os
import yaml
import pathspec
import functools

from collections.abc import Mapping
from typing import List, Dict, Any, Callable
from functools import cached_property

DEFAULT_CONFIG = {
    "file_handlers": {
        "yaml": "loren.parsers.yaml_parser.YamlParser",
        "yml": "loren.parsers.yaml_parser.YamlParser",
        "json": "loren.parsers.json_parser.JSONParser",
        "py": "loren.parsers.python_parser.PyParser",
        "csv": "loren.parsers.csv_parser.CSVParser",
        "tsv": "loren.parsers.csv_parser.TSVParser",
        "j2": "loren.file_loaders.jinja2_loader.Jinja2Loader",
        "jinja2": "loren.file_loaders.jinja2_loader.Jinja2Loader",
        "jpg": "loren.file_loaders.base64_loader.URLSafeBase64Loader",
        "png": "loren.file_loaders.base64_loader.URLSafeBase64Loader",
        "*": "loren.file_loaders.text_loader.TextLoader",
        "*": "loren.parsers.text_parser.TextParser",
    },
    "ignore": [
        ".loren.yml",
        ".DS_Store",
        "_*",
        ".*",
        "folder_b/"
    ]
}

def recursive_dict_update(d: dict, u: dict) -> None:
    for k, v in u.items():
        if k not in d:
            d[k] = v
        elif isinstance(v, Mapping):
            recursive_dict_update(d[k], v)


class Lodict(dict):
    def __new__(cls, root_path=".", lazy=True, preserve_file_suffix=False, config=None):

        if isinstance(root_path, str):
            return super().__new__(cls, root_path, lazy, preserve_file_suffix, config)
        
        if isinstance(root_path, dict):
            return {
                k: super().__new__(v, lazy, preserve_file_suffix, config)
                for k, v in root_path.items()
            }

        if isinstance(root_path, list):
            return [
                super().__new__(v, lazy, preserve_file_suffix, config)
                for v in root_path
            ]
        

    def _ignore_func(self, item):
        return self.config["ignore"].match_file(
            item.path[len(self.config["base_path"])+1:] + ("/" if item.is_dir() else "")
        )

    def __init__(self, root_path=".", lazy=True, preserve_file_suffix=False, config=None):
        self.root_path = root_path.rstrip("/")
        self.lazy = lazy
        self.preserve_file_suffix = preserve_file_suffix
        self.config = config
        if self.config is None:
            try:
                with open(os.path.join(self.root_path, ".loren.yml"), "r") as f:
                    self.config = yaml.safe_load(f)
            except FileNotFoundError:
                self.config = DEFAULT_CONFIG
                        
            self.config["ignore"] = pathspec.PathSpec.from_lines(
                'gitwildmatch', 
                self.config.get("ignore", [])
            )
            self.config["base_path"] = self.root_path
        
        for key, sources in self.sources.items():
            if lazy:
                self[key] = NotInitiated(sources)
            else:
                self._init_key(key, sources)      

    def _init_keys(self):
        for key, value in self.items():
            if type(value) == NotInitiated:
                self._init_key(key, value.sources)

    def _init_key(self, key, sources):
        for source in sources:
            if key not in self or type(super().__getitem__(key)) == NotInitiated:
                self[key] = self._file_loader(source)
            else:
                recursive_dict_update(super().__getitem__(key), self._file_loader(source))

    def __getitem__(self, key):
        if self.lazy:
            result = super().__getitem__(key)
            if type(result) == NotInitiated:
                self._init_key(key, result.sources)
                return super().__getitem__(key)
            else:
                return result
        else:
            return super().__getitem__(key)

    def _file_loader(self, path: str) -> Dict[str, Any]:
        if os.path.isdir(path):
            return Lodict(
                root_path=path, 
                lazy=self.lazy,
                preserve_file_suffix=self.preserve_file_suffix,
                config=self.config
            )
        with open(path, "r") as file:
            return yaml.safe_load(file.read())

    def to_dict(self):
        self._init_keys()
        for key, value in self.items():
            if isinstance(value, Lodict):
                self[key] = value.to_dict()
        return dict(self)

    @cached_property
    def sources(self):
        source_files = {}
        for item in os.scandir(self.root_path):
            if self._ignore_func(item):
                continue
                
            item_name = item.name
            
            if not self.preserve_file_suffix:
                item_name = item_name.split(".")[0]
            
            source_files.setdefault(item_name, []).append(item.path)
        return source_files

    def __repr__(self):
        return f"{self.__class__.__name__}({super().__repr__()})"

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError as e:
            if default:
                return default
            else:
                raise e

    def __getattribute__(self, name):
        return super().__getattribute__(name)

    def items(self):
        for key in self.keys():
            yield key, self.__getitem__(key)


class NotInitiated(object):
    def __init__(self, sources):
        self.sources = sources



loader = Lodict(".", lazy=True, preserve_file_suffix=False)
print(loader)
