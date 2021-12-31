import os

from loren.parser import (
    get_config,
    get_parsers,
    DEFAULT_PARSERS,
    get_loaders,
    DEFAULT_LOADERS,
    get_loader_class,
    get_parser_class,
    get_ignore,
    parse,
    validate
)

from loren.file_loaders.base_loader import BaseLoader
from loren.parsers.base_parser import BaseParser
from loren.new_parser import LorenDict



def create_context(tmp_path):
    with open(f"{tmp_path}/.loren.yaml", "w+") as conf_file:
        conf_file.write("parsers:\n")
        conf_file.write("  yaml: loren.parsers.yaml_parser.YamlParser\n")
        conf_file.write("loaders:\n")
        conf_file.write('  "*": loren.file_loaders.text_loader.TextLoader\n') # noqa E501
    with open(f"{tmp_path}/.lorenignore", "w+") as ignore_file:
        ignore_file.write(".*\n_*")
    with open(f"{tmp_path}/_ignored_underscore.py", "w+") as ignored_file:
        ignored_file.write("\n")

    os.makedirs(f"{tmp_path}/level_1/level_2")
    with open(f"{tmp_path}/level_1/level_2/_ignored_underscore_2.py", "w+") as ignored_file: # noqa E501
        ignored_file.write("\n")

    with open(f"{tmp_path}/level_1/level_2/file.yaml", "w+") as yaml_file_subdir: # noqa E501
        yaml_file_subdir.write("foo: bar")

    with open(f"{tmp_path}/level_1/file.yaml", "w+") as yaml_file_subdir: # noqa E501
        yaml_file_subdir.write("bar: baz")


def test_parse(tmp_path):
    create_context(tmp_path)
    conf = LorenDict(str(tmp_path), lazy=False, preserve_file_suffix=False)
    assert conf["level_1"].source == {
        'bar': 'baz',
        '_path':
        f'{tmp_path}/level_1/file.yaml'
    }

    assert conf["level_1"]["level_2"]["file"] == {
        'foo': 'bar',
        '_path': f'{tmp_path}/level_1/level_2/file.yaml'
    }
