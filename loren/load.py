
import os
import yaml
import pathspec
import functools
import importlib

from collections.abc import Mapping
from typing import Dict, Any, Type
from functools import cached_property
from parsers.base_parser import BaseParser
from file_reader import LorenFileReader



@functools.lru_cache()
def get_parser_class(class_ref) -> Type[BaseParser]:
    return getattr(
        importlib.import_module(".".join(class_ref.split(".")[:-1])),
        class_ref.split(".")[-1]
    )

def recursive_dict_update(d: dict, u: dict) -> None:
    for k, v in u.items():
        if k not in d:
            d[k] = v
        elif isinstance(v, Mapping):
            recursive_dict_update(d[k], v)

class NotInitiated(object):
    def __init__(self, sources):
        self.sources = sources

class LorenDict(dict):
    def __new__(cls, root_path=".", lazy=True, preserve_file_suffix=False, config=None):

        if isinstance(root_path, str):
            return super().__new__(cls, root_path, lazy, preserve_file_suffix, config)
        
        elif isinstance(root_path, dict):
            return {
                k: super().__new__(cls, v, lazy, preserve_file_suffix, config)
                for k, v in root_path.items()
            }

        elif isinstance(root_path, list):
            return [
                super().__new__(cls, v, lazy, preserve_file_suffix, config)
                for v in root_path
            ]

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
            return LorenDict(
                root_path=path, 
                lazy=self.lazy,
                preserve_file_suffix=self.preserve_file_suffix,
                config=self.config
            )
        file_contents = LorenFileReader.load(path)
        parsed_file_contents = file_contents
        for file_extension in reversed(path.split(".")[1:]):
            if isinstance(parsed_file_contents, dict):
                parsed_file_contents = parsed_file_contents["file_contents"]
            
            parser_class_path = self.config["file_handlers"].get(
                file_extension,
                self.config["file_handlers"]["*"]
            )
            parser_class = get_parser_class(parser_class_path)
            parsed_file_contents = parser_class.parse(
                file_contents=parsed_file_contents,
                file_path=path,
                root_path=self.config["base_path"]
            )
        return parsed_file_contents

    def to_dict(self):
        self._init_keys()
        for key, value in self.items():
            if isinstance(value, LorenDict):
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
    
    def _ignore_func(self, item):
        return self.config["ignore"].match_file(
            item.path[len(self.config["base_path"])+1:] + ("/" if item.is_dir() else "")
        )

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

    def validate(self, schema_path: str) -> None:
        import jsonschema
        import json

        with open(schema_path, "r") as schema:
            jsonschema.validate(self.to_dict(), json.load(schema))

print(LorenDict("tmp/test", lazy=False, preserve_file_suffix=False))