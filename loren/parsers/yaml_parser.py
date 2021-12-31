import yaml
from typing import Dict, Any
from parsers.base_parser import BaseParser


class YamlParser(BaseParser):

    @staticmethod
    def parse(file_contents: str, **kwargs) -> Dict[str, Any]:
        return yaml.safe_load(file_contents)
