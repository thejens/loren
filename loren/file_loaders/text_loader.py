from .base_loader import BaseLoader


class TextLoader(BaseLoader):

    @staticmethod
    def load(file_path, root_path, **kwargs) -> str:
        with open(file_path, "r") as file:
                try:
                    return file.read()
                except Exception as e:
                    print(f"Exception raised when opening {file_path}")
                    raise e
