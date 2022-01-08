import yaml
from loren.utilities.configuration import (
    DEFAULT_CONFIG,
    LorenConfiguration
)
from importlib import import_module
from pathspec.pathspec import PathSpec
from pathlib import PosixPath

def test_default_config() -> None:
    assert isinstance(DEFAULT_CONFIG, dict)
    assert "file_handlers" in DEFAULT_CONFIG
    assert isinstance(DEFAULT_CONFIG["file_handlers"], dict)
    assert (
        DEFAULT_CONFIG["file_handlers"]["*"] == "loren.parsers.text_parser.TextParser"
    )
    assert "ignore" in DEFAULT_CONFIG
    assert isinstance(DEFAULT_CONFIG["ignore"], list)
    assert len(DEFAULT_CONFIG["ignore"]) > 0


def test_import_handlers() -> None:
    for handler in DEFAULT_CONFIG["file_handlers"].values():
        import_module(".".join(handler.split(".")[:-1]))


def test_init_configuration(tmp_path: PosixPath) -> None:
    LorenConfiguration(str(tmp_path)).dump_configuration()
    with open(f"{tmp_path}/.loren.yml", "r+") as configuration:
        config = yaml.safe_load(configuration)
    assert config == DEFAULT_CONFIG


def test_get_configuration_no_file(tmp_path: PosixPath) -> None:
    conf = LorenConfiguration(str(tmp_path))
    assert conf.base_path == str(tmp_path)
    assert isinstance(conf.ignore_paths, PathSpec)


def test_get_configuration_file_exists(tmp_path: PosixPath) -> None:
    with open(f"{tmp_path}/.loren.yml", "w+", encoding="utf-8") as configuration:
        configuration.write("ignore: ['templates*']")

    conf = LorenConfiguration(str(tmp_path))
    expected_conf = DEFAULT_CONFIG.copy()
    expected_conf["base_path"] = str(tmp_path)
    expected_conf["ignore"] = ["templates*"]
    assert conf.ignore_paths.match_file("templates/some_template.yml")
