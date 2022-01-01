import yaml
from typing import Dict, Any
from loren.parsers.base_parser import BaseParser


class YamlParser(BaseParser):
    
    @staticmethod
    def parse(data: Dict[str, str], **kwargs) -> Dict[str, Any]:
        try:
            file_contents = data["file_contents"].decode("utf-8")
        except AttributeError:
            file_contents = data["file_contents"]
        return yaml.safe_load(file_contents)
