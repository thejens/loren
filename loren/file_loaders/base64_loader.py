import base64
from .base_loader import BaseLoader


class URLSafeBase64Loader(BaseLoader):

    @staticmethod
    def load(file_path, root_path, **kwargs) -> str:
        with open(file_path, "rb") as file:
            return base64.urlsafe_b64encode(file.read()).decode("utf-8")


class Base64Loader(BaseLoader):

    @staticmethod
    def load(file_path, root_path, **kwargs) -> str:
        with open(file_path, "rb") as file:
            return base64.b64encode(file.read()).decode("utf-8")
