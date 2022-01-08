import os
try:
    import json
    import jsonschema
except ImportError:
    pass  
from collections.abc import Mapping
from typing import Dict, Any, List
from functools import cached_property
from loren.utilities.file_reader import LorenFileReader
from loren.utilities.configuration import LorenConfiguration


def recursive_dict_update(default: Mapping, update: Mapping) -> None:
    for key, value in update.items():
        if key not in default:
            default[key] = value
        elif isinstance(value, Mapping):
            recursive_dict_update(default[key], value)


class NotInitiated():
    def __init__(self, sources):
        self.sources = sources


class LorenDict(dict):
    def __init__(
        self,
        root_path=".",
        lazy=True,
        preserve_file_suffix=False,
        config=None,
        additional_args=None,
    ):
        self.lazy = lazy
        self.preserve_file_suffix = preserve_file_suffix
        if additional_args is None:
            self.additional_args = {}
        else:
            self.additional_args = additional_args

        if isinstance(root_path, Mapping):
            for key, path in root_path.items():
                self[key] = LorenDict(
                    path, lazy, preserve_file_suffix, config, additional_args
                )

        elif isinstance(root_path, (set, list)):
            for i, path in enumerate(root_path):
                self[i] = LorenDict(
                    path, lazy, preserve_file_suffix, config, additional_args
                )

        else:
            root_path = str(root_path)
            if os.path.isfile(root_path):
                self.config = LorenConfiguration(path=root_path)
                self.sources = [root_path]
                recursive_dict_update(self, self._file_loader(root_path))

            else:
                self.root_path = root_path.rstrip("/")
                if config is None:
                    self.config = LorenConfiguration(path=root_path)
                else:
                    self.config = config

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
                recursive_dict_update(
                    super().__getitem__(key), self._file_loader(source)
                )

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
                config=self.config,
                additional_args=self.additional_args,
            )
        file_contents = LorenFileReader.read(path)
        for file_extension in reversed(path.strip(".").split(".")[1:]):
            parser_class = self.config.get_parser_class(file_extension)
            file_contents = parser_class.parse(
                data=file_contents,
                file_path=path,
                root_path=self.config.base_path,
                additional_args=self.additional_args,
            )
        return file_contents

    def to_dict(self) -> Dict[str, Any]:
        self._init_keys()
        for key, value in self.items():
            if isinstance(value, LorenDict):
                self[key] = value.to_dict()
        return dict(self)

    @cached_property
    def sources(self) -> Dict[str, List[str]]:
        source_files: Dict[str, List[str]] = {}
        for item in os.scandir(self.root_path):
            if self.config.is_ignored_file(item):
                continue

            item_name = item.name

            if not self.preserve_file_suffix:
                item_name = item_name.split(".")[0]

            source_files.setdefault(item_name, []).append(item.path)
        return source_files

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({super().__repr__()})"

    def get(self, key: Any, default: Any=None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError as e:
            if default:
                return default
            else:
                raise e

    def items(self):
        for key in self.keys():
            yield key, self.__getitem__(key)

    def validate(self, schema_path: str) -> None:
        with open(schema_path, "r") as schema:
            jsonschema.validate(self.to_dict(), json.load(schema))
