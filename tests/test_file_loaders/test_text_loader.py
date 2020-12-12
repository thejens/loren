import os
from omniparse.file_loaders.base_loader import BaseLoader
from omniparse.file_loaders.text_loader import TextLoader


def test_class():
    assert issubclass(TextLoader, BaseLoader)


def test_file_read(tmp_path):
    os.makedirs(f"{tmp_path}/test/")
    s = "foo: 123"
    with open(f"{tmp_path}/test/conf.yaml", "w+") as yaml_file:
        yaml_file.write("foo: 123")
    assert TextLoader.load(
      f"{tmp_path}/test/conf.yaml",
      tmp_path
    ) == s
