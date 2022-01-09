# pylint: disable=too-many-arguments
# pylint: disable=missing-class-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
try:
    import json
    import jsonschema
except ImportError:
    pass
from pathlib import Path
from typing import Dict, Any, List, Union, Optional
from loren.utilities.file_reader import LorenFileReader
from loren.utilities.configuration import LorenConfiguration


class LorenDict(dict):
    def __new__(
        cls,  # pylint: disable=unused-argument
        path: Union[str, Path] = ".",
        paths: Union[
            Dict[Union[int, str], Union[str, Path]], List[Union[str, Path]]
        ] = None,
        **kwargs: Any,
    ) -> "LorenDict":
        if not paths:
            if isinstance(path, str):
                path = Path(path)
            return super().__new__(LorenDict)

        elif isinstance(paths, list):
            if path:
                paths.append(path)
            paths = [Path(p) if not isinstance(p, Path) else p for p in paths]
            return super().__new__(LorenDictList)

        elif isinstance(paths, dict):
            if path and not "path" in paths:
                paths["path"] = path

            return super().__new__(LorenDictMapping)

        raise TypeError

    def initiate(self) -> None:
        is_file = self.path.is_file()

        if self.input_configuration:
            self.configuration = self.input_configuration
        else:
            if is_file:
                self.configuration = LorenConfiguration(self.path.parent)
            else:
                self.configuration = LorenConfiguration(self.path)

        if is_file:
            self.initiate_file()
        else:
            self.initiate_folder()

    def initiate_folder(self) -> None:
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

        self.is_initiated = True

    def initiate_file(self) -> None:
        print(f"Loading {self.path}")
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
        if populated_keys:
            super().__init__(populated_keys)
        else:
            super().__init__()

        self.lazy = lazy
        self.preserve_file_suffix = preserve_file_suffix
        self.additional_args = additional_args
        self.key = key
        self.is_initiated = False
        self.path: Path = Path(path) if not isinstance(path, Path) else path
        self.key = key
        self.input_configuration: Optional[LorenConfiguration] = configuration

        if not lazy:
            self.initiate()

    def __getitem__(self, key: str) -> Any:
        if not self.is_initiated:
            self.initiate()
        return super().__getitem__(key)

    def __repr__(self) -> str:
        if self.is_initiated:
            return super().__repr__()
        else:
            return f"{self.__class__.__name__}(Not Initiated)"

    def validate(self, schema_path: str) -> None:
        with open(schema_path, "r", encoding="utf-8") as schema:
            jsonschema.validate(self, json.load(schema))



class LorenDictList(LorenDict):
    def __init__(
        self,
        paths: List[Path],
        lazy: bool = True,
        preserve_file_suffix: bool = False,
        additional_args: dict = None,
    ):
        populated_keys: Dict[int, LorenDict] = {}
        for i, path in enumerate(paths):
            populated_keys[i] = LorenDict(
                path=path,
                key=i,
                lazy=lazy,
                preserve_file_suffix=preserve_file_suffix,
                additional_args=additional_args,
            )
        super().__init__(
            lazy=lazy,
            preserve_file_suffix=preserve_file_suffix,
            additional_args=additional_args,
            populated_keys=populated_keys,
        )


class LorenDictMapping(LorenDict):
    def __init__(
        self,
        paths: Dict[str, Path],
        lazy: bool = True,
        preserve_file_suffix: bool = False,
        additional_args: dict = None,
    ):
        populated_keys: Dict[str, LorenDict] = {}
        for key, path in paths.items():
            populated_keys[key] = LorenDict(
                path=path,
                key=key,
                lazy=lazy,
                preserve_file_suffix=preserve_file_suffix,
                additional_args=additional_args,
            )
        super().__init__(
            lazy=lazy,
            preserve_file_suffix=preserve_file_suffix,
            additional_args=additional_args,
            populated_keys=populated_keys,
        )


root_paths = {
    "a": Path("examples").joinpath("template_airflow_dag").joinpath("config"),
    "b": Path("examples").joinpath("config_basic").joinpath("input_config")
}
conf = LorenDict(
    paths=root_paths, lazy=True, preserve_file_suffix=False
)

#conf.initiate_all()
print(conf.to_json())