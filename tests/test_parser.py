import os

from parender.parser import (
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

from parender.file_loaders.base_loader import BaseLoader
from parender.parsers.base_parser import BaseParser


def create_context(tmp_path):
    with open(f"{tmp_path}/.parender.yaml", "w+") as conf_file:
        conf_file.write("parsers:\n")
        conf_file.write("  yaml: parender.parsers.yaml_parser.YamlParser\n")
        conf_file.write("loaders:\n")
        conf_file.write('  "*": parender.file_loaders.text_loader.TextLoader\n') # noqa E501
    with open(f"{tmp_path}/.parenderignore", "w+") as ignore_file:
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


def test_get_config(tmp_path):
    create_context(tmp_path)
    conf = get_config(tmp_path)
    assert conf["parsers"]["yaml"] == "parender.parsers.yaml_parser.YamlParser" # noqa E501


def test_get_default_config():
    conf = get_config("/non/existing/path")
    assert conf == {}


def test_get_parsers(tmp_path):
    create_context(tmp_path)
    parsers = get_parsers(tmp_path)
    assert parsers["yaml"] == "parender.parsers.yaml_parser.YamlParser"
    assert parsers != DEFAULT_PARSERS


def test_get_default_parsers():
    parsers = get_parsers("/")
    assert parsers == DEFAULT_PARSERS


def test_get_loaders(tmp_path):
    create_context(tmp_path)
    loaders = get_loaders(tmp_path)
    assert loaders["*"] == "parender.file_loaders.text_loader.TextLoader"
    assert loaders != DEFAULT_LOADERS


def test_get_default_loaders():
    loaders = get_loaders("/")
    assert loaders == DEFAULT_LOADERS


def test_get_loader_class():
    assert issubclass(
        get_loader_class("parender.file_loaders.text_loader.TextLoader"),
        BaseLoader
    )


def test_get_parser_class():
    assert issubclass(
        get_parser_class("parender.parsers.yaml_parser.YamlParser"),
        BaseParser
    )


def test_get_ignore(tmp_path):
    create_context(tmp_path)
    ignore = get_ignore(tmp_path)
    assert ignore('.parender.yaml')
    assert ignore('.parenderignore')
    assert ignore('_ignored_underscore.py')
    assert ignore('level_1/level_2/_ignored_underscore_2.py')
    assert not ignore('level_1/level_2/file.yaml')


def test_parse(tmp_path):
    create_context(tmp_path)
    conf = parse(str(tmp_path))
    assert conf["level_1"]["file"] == {
        'bar': 'baz',
        '_path':
        f'{tmp_path}/level_1/file.yaml'
    }

    assert conf["level_1"]["level_2"]["file"] == {
        'foo': 'bar',
        '_path': f'{tmp_path}/level_1/level_2/file.yaml'
    }


def test_validate(tmp_path):
    with open(f"{tmp_path}/correct_schema.yaml", "w+") as schema_file:
        schema_file.write("{\n")
        schema_file.write('"$schema": "http://json-schema.org/draft-07/schema",\n') # noqa E501
        schema_file.write('"type": "object",\n')
        schema_file.write('"properties": {\n')
        schema_file.write('"conf": {"type": "object",\n')
        schema_file.write('"properties": {"foo": {"type": "integer"}}\n')
        schema_file.write('}\n')
        schema_file.write('},\n')
        schema_file.write('"additionalProperties": false\n')
        schema_file.write('}')
        schema_file.seek(0)
        print(schema_file.read())

    os.makedirs(f"{tmp_path}/test/")
    with open(f"{tmp_path}/test/conf.yaml", "w+") as yaml_file:
        yaml_file.write("foo: 123")

    print(parse(str(tmp_path)+"/test/"))
    validate(
        parse(str(tmp_path)+"/test/"),
        f"{tmp_path}/correct_schema.yaml"
    )
