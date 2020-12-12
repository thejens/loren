from .base_loader import BaseLoader


class TextLoader(BaseLoader):

    @staticmethod
    def load(file_path, root_path, **kwargs) -> str:
        with open(file_path, "r") as file:
            return file.read()
