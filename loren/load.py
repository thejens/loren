# pylint: disable=too-many-arguments
# pylint: disable=missing-class-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
try:
    import json
    import jsonschema
except ImportError:
    pass
import yaml
from pathlib import Path
from typing import Dict, Any, List, Union, Optional
from loren.utilities.file_reader import LorenFileReader
from loren.utilities.configuration import LorenConfiguration


class LorenDict(dict):
    path: Path = NotImplemented
    path_list: List[Path] = NotImplemented
    path_dict: Dict[Union[str, int], Path] = NotImplemented

    def __new__(
        cls,  # pylint: disable=unused-argument
        path: Union[
            Dict[Union[int, str], Union[str, Path]],
            List[Union[str, Path]],
            Union[str, Path],
        ] = None,
        **kwargs: Any,
    ) -> "LorenDict":
        if path is None or isinstance(path, (str, Path)):
            if path:
                typed_path: Path = Path(path)
            else:
                typed_path = Path(".")

            if typed_path.is_file():
                return super().__new__(LorenDictFile)
            else:
                return super().__new__(LorenDictFolder)

        elif isinstance(path, list):
            return super().__new__(LorenDictList)

        elif isinstance(path, dict):
            return super().__new__(LorenDictMapping)

        raise TypeError

    def __init__(
        self,  # pylint: disable=unused-argument
        key: Union[str, int] = -1,
        lazy: bool = True,
        preserve_file_suffix: bool = False,
        additional_args: dict = None,
        populated_keys: dict = None,
        configuration: LorenConfiguration = None,
        **kwargs: Any,
    ):
        self.is_initiated = False
        self.configuration = configuration
        if populated_keys:
            super().__init__(populated_keys)
        else:
            super().__init__()
        self.lazy = lazy
        self.preserve_file_suffix = preserve_file_suffix
        self.additional_args = additional_args
        self.key = key

        if not lazy:
            self._initiate()

    def initiate(self) -> None:
        raise NotImplementedError

    def _initiate(self) -> None:
        if not self.is_initiated:
            self.initiate()
        self.is_initiated = True

    def initiate_all(self) -> None:
        if not self.is_initiated:
            self.initiate()
        for child in self.values():
            if isinstance(child, LorenDict):
                child.initiate_all()

    def to_dict(self) -> Dict[str, Any]:
        self.initiate_all()
        for key, child in self.items():
            if isinstance(child, LorenDict):
                self[key] = child.to_dict()
        self["_path"] = str(self.path)
        return dict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def __getitem__(self, key: str) -> Any:
        if not self.is_initiated:
            self._initiate()
        return super().__getitem__(key)

    def __repr__(self) -> str:
        if self.is_initiated:
            return f"{self.__class__.__name__}({super().__repr__()})"
        else:
            return f"{self.__class__.__name__}(Not Initiated)"

    def validate(self, schema_path: str) -> None:
        with open(schema_path, "r", encoding="utf-8") as schema:
            if schema_path.endswith(".json"):
                jsonschema.validate(self, json.load(schema))
            elif schema_path.endswith(".yaml") or schema_path.endswith(".yml"):
                jsonschema.validate(self, yaml.safe_load(schema))
            else:
                raise NameError(
                    "Schema file invalid, supported name suffixes are [json, yml, yaml]"
                )


class LorenDictFS(LorenDict):
    def initiate(self) -> None:
        raise NotImplementedError

    def __init__(
        self,
        path: Union[str, Path] = ".",
        key: Union[str, int] = -1,
        lazy: bool = True,
        preserve_file_suffix: bool = False,
        additional_args: dict = None,
        populated_keys: dict = None,
        configuration: LorenConfiguration = None,
    ):
        self.path = Path(path)
        super().__init__(
            key=key,
            lazy=lazy,
            preserve_file_suffix=preserve_file_suffix,
            additional_args=additional_args,
            populated_keys=populated_keys,
            configuration=configuration,
        )


class LorenDictFile(LorenDictFS):
    def initiate(self) -> None:
        if not self.configuration:
            self.configuration = LorenConfiguration(self.path.parent)

        file_contents = LorenFileReader.read(self.path)
        for file_extension in reversed(str(self.path).strip(".").split(".")[1:]):
            parser_class = self.configuration.get_parser_class(file_extension)
            file_contents = parser_class.parse(
                data=file_contents,
                file_path=self.path,
                root_path=self.configuration.base_path,
                additional_args=self.additional_args,
            )
        for key, value in file_contents.items():
            self[key] = value


class LorenDictFolder(LorenDictFS):
    def initiate(self) -> None:
        if not self.configuration:
            self.configuration = LorenConfiguration(self.path)

        files: Dict[str, List[Path]] = {}
        for file in self.path.iterdir():
            if self.configuration.is_ignored_file(file):
                continue

            item_name = file.name

            if not self.preserve_file_suffix:
                item_name = item_name.split(".")[0]

            files.setdefault(item_name, []).append(file)

        for key, file_list in files.items():
            for file in file_list:
                self[key] = LorenDict(
                    path=file,
                    key=key,
                    lazy=self.lazy,
                    preserve_file_suffix=self.preserve_file_suffix,
                    additional_args=self.additional_args,
                    populated_keys=self.get(key, {}),
                    configuration=self.configuration,
                )


class LorenDictList(LorenDict):
    def initiate(self) -> None:
        for i, path in enumerate(self.paths):
            self[i] = LorenDict(
                path=path,
                key=i,
                lazy=self.lazy,
                preserve_file_suffix=self.preserve_file_suffix,
                additional_args=self.additional_args,
            )

    def __init__(
        self,
        path: List[Union[str, Path]],
        lazy: bool = True,
        preserve_file_suffix: bool = False,
        additional_args: dict = None,
        populated_keys: dict = None,
    ):
        self.paths = [Path(p) for p in path]
        super().__init__(
            lazy=lazy,
            preserve_file_suffix=preserve_file_suffix,
            additional_args=additional_args,
            populated_keys=populated_keys,
        )


class LorenDictMapping(LorenDict):
    def initiate(self) -> None:
        for key, path in self.paths.items():
            self[key] = LorenDict(
                path=path,
                key=key,
                lazy=self.lazy,
                preserve_file_suffix=self.preserve_file_suffix,
                additional_args=self.additional_args,
            )

    def __init__(
        self,
        path: Dict[str, Union[str, Path]],
        lazy: bool = True,
        preserve_file_suffix: bool = False,
        additional_args: dict = None,
        populated_keys: dict = None,
    ):
        self.paths = {key: Path(path) for key, path in path.items()}
        super().__init__(
            lazy=lazy,
            preserve_file_suffix=preserve_file_suffix,
            additional_args=additional_args,
            populated_keys=populated_keys,
        )
