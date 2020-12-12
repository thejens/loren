import os
from omniparse.file_loaders.base_loader import BaseLoader
from omniparse.file_loaders.jinja2_loader import Jinja2Loader


def test_class():
    assert issubclass(Jinja2Loader, BaseLoader)


def test_file_read(tmp_path):
    os.makedirs(f"{tmp_path}/test/")
    with open(f"{tmp_path}/test/conf.yaml.j2", "w+") as yaml_file:
        yaml_file.write("{% for i in range(10) %}1{% endfor %}")
    assert Jinja2Loader.load(
      f"{tmp_path}/test/conf.yaml.j2",
      str(tmp_path)
    ) == "1"*10
