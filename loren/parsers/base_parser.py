# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=too-few-public-methods
from typing import Dict, Any
from pathlib import Path


class BaseParser:
    @classmethod
    def _parse(
        cls,
        data: Dict[str, str],
        file_path: Path = None,  # pylint: disable=unused-argument
        root_path: Path = None,  # pylint: disable=unused-argument
        additional_args: Dict = None,  # pylint: disable=unused-argument
    ) -> Dict[str, Any]:
        return data

    @classmethod
    def parse(cls, data: Dict[str, str], **kwargs: Any) -> Dict[str, Any]:
        return cls._parse(data, **kwargs)
