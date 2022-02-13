# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from pathlib import Path
from unittest.mock import patch
from typing import Any
import sys
import json
import yaml
from loren.__main__ import (
    action_init,
    action_render,
    action_validate,
    action_print,
    action_dump,
)
from loren.utilities.configuration import DEFAULT_CONFIG

EXAMPLES_DIR = Path(__file__).parent.parent.joinpath("examples")


def test_render(tmp_path: Path) -> None:
    with patch.object(
        sys,
        "argv",
        [
            "render",
            "-t",
            str(
                EXAMPLES_DIR.joinpath(
                    "template_basic", "input_template", "basic_template.html.j2"
                )
            ),
            "-c",
            str(EXAMPLES_DIR.joinpath("template_basic", "input_config")),
            "-o",
            str(tmp_path),
        ],
    ):
        action_render()

    with open(
        tmp_path.joinpath("basic_template.html"), "r", encoding="utf-8"
    ) as result_file, open(
        EXAMPLES_DIR.joinpath("template_basic", "example_result.html"), encoding="utf-8"
    ) as expected_result_file:
        assert result_file.read() == expected_result_file.read()


def test_validate_json(capsys: Any) -> None:
    with patch.object(
        sys,
        "argv",
        [
            "validate",
            "-c",
            str(EXAMPLES_DIR.joinpath("config_with_jsonschema", "input_config")),
            "-s",
            str(EXAMPLES_DIR.joinpath("config_with_jsonschema", "example_schema.json")),
        ],
    ):
        action_validate()
    assert capsys.readouterr().out == "Configuration is valid\n"


def test_validate_yaml(capsys: Any) -> None:
    with patch.object(
        sys,
        "argv",
        [
            "validate",
            "-c",
            str(EXAMPLES_DIR.joinpath("config_with_jsonschema", "input_config")),
            "-s",
            str(EXAMPLES_DIR.joinpath("config_with_jsonschema", "example_schema.yaml")),
        ],
    ):
        action_validate()
    assert capsys.readouterr().out == "Configuration is valid\n"


def test_print(capsys: Any) -> None:
    with patch.object(
        sys,
        "argv",
        [
            "print",
            "-c",
            str(EXAMPLES_DIR.joinpath("config_basic", "input_config")),
        ],
    ):
        action_print()
    with open(
        EXAMPLES_DIR.joinpath("config_basic", "example_result.json"), encoding="utf-8"
    ) as expected_result_file:
        assert json.loads(capsys.readouterr().out) == json.loads(
            expected_result_file.read()
        )


def test_dump(tmp_path: Path) -> None:
    with patch.object(
        sys,
        "argv",
        [
            "dump",
            "-c",
            str(EXAMPLES_DIR.joinpath("config_basic", "input_config")),
            "-o",
            str(tmp_path.joinpath("out.json")),
        ],
    ):
        action_dump()
    with open(
        tmp_path.joinpath("out.json"), "r", encoding="utf-8"
    ) as result_file, open(
        EXAMPLES_DIR.joinpath("config_basic", "example_result.json"), encoding="utf-8"
    ) as expected_result_file:
        assert json.loads(result_file.read()) == json.loads(expected_result_file.read())


def test_init(tmp_path: Path) -> None:
    with patch.object(sys, "argv", ["init", "-c", str(tmp_path)]):
        action_init()

    with open(tmp_path.joinpath(".loren.yml"), "r", encoding="utf-8") as conf:
        assert yaml.safe_load(conf) == DEFAULT_CONFIG


def test_init_two_paths(tmp_path: Path) -> None:
    with patch.object(
        sys,
        "argv",
        [
            "init",
            "-c",
            str(tmp_path.joinpath("dir_a")),
            "-c",
            str(tmp_path.joinpath("dir_b")),
        ],
    ):
        action_init()

    with open(
        tmp_path.joinpath("dir_a").joinpath(".loren.yml"), "r", encoding="utf-8"
    ) as conf:
        assert yaml.safe_load(conf) == DEFAULT_CONFIG

    with open(
        tmp_path.joinpath("dir_b").joinpath(".loren.yml"), "r", encoding="utf-8"
    ) as conf:
        assert yaml.safe_load(conf) == DEFAULT_CONFIG


def test_init_two_paths_dict(tmp_path: Path) -> None:
    with patch.object(
        sys,
        "argv",
        [
            "init",
            "-c",
            f'a:{str(tmp_path.joinpath("dir_a"))}',
            "-c",
            f'b:{str(tmp_path.joinpath("dir_b"))}',
        ],
    ):
        action_init()

    with open(
        tmp_path.joinpath("dir_a").joinpath(".loren.yml"), "r", encoding="utf-8"
    ) as conf:
        assert yaml.safe_load(conf) == DEFAULT_CONFIG

    with open(
        tmp_path.joinpath("dir_b").joinpath(".loren.yml"), "r", encoding="utf-8"
    ) as conf:
        assert yaml.safe_load(conf) == DEFAULT_CONFIG
