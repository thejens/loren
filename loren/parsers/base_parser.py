from typing import Dict, Any


class BaseParser(object):
    @classmethod
    def parse(cls, file_contents: str, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError()
