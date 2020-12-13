from typing import Dict, Any


class BaseParser(object):

    @staticmethod
    def parse(file_contents: str) -> Dict[str, Any]:
        raise NotImplementedError()
