import os
from omniparse.file_loaders.base_loader import BaseLoader
from omniparse.file_loaders.base64_loader import Base64Loader


def test_class():
    assert issubclass(Base64Loader, BaseLoader)


def test_file_read(tmp_path):
    os.makedirs(f"{tmp_path}/test/")
    with open(f"{tmp_path}/test/conf.yaml.j2", "wb+") as yaml_file:
        yaml_file.write(b"some_bytes")

    assert Base64Loader.load(
      f"{tmp_path}/test/conf.yaml.j2",
      str(tmp_path)
    ) == "c29tZV9ieXRlcw=="
