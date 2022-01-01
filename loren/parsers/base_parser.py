from typing import Dict, Any


class BaseParser(object):
    @classmethod
    def parse(cls, data: Dict[str, str], **kwargs) -> Dict[str, Any]:
        raise NotImplementedError()
