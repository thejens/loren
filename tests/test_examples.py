# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

from pathlib import Path
from unittest import TestCase
import json
import os
import pytest
from jsonschema.exceptions import ValidationError
from loren.load import LorenDict
from loren.render import render

EXAMPLES_DIR = Path(__file__).parent.parent.joinpath("examples")


def test_examples_path() -> None:
    assert EXAMPLES_DIR.is_dir()


def test_config_basic() -> None:
    configuration_path = EXAMPLES_DIR.joinpath("config_basic")
    conf = LorenDict(
        configuration_path.joinpath("input_config"),
        lazy=False,
        preserve_file_suffix=False,
    )
    assert conf
    with open(
        configuration_path.joinpath("example_result.json"), "r", encoding="utf-8"
    ) as expected_result_file:
        expected_result = json.load(expected_result_file)
    TestCase().assertDictEqual(conf, expected_result)


def test_config_advanced() -> None:
    configuration_path = EXAMPLES_DIR.joinpath("config_advanced")
    conf = LorenDict(
        configuration_path.joinpath("input_config"),
        lazy=False,
        preserve_file_suffix=False,
    )
    assert conf
    with open(
        configuration_path.joinpath("example_result.json"), "r", encoding="utf-8"
    ) as expected_result_file:
        expected_result = json.load(expected_result_file)
    TestCase().assertDictEqual(conf, expected_result)


def test_config_with_jinja2() -> None:
    configuration_path = EXAMPLES_DIR.joinpath("config_with_jinja2")
    conf = LorenDict(
        configuration_path.joinpath("input_config"),
        lazy=False,
        preserve_file_suffix=False,
        additional_args={"parameter_from_call": "test"},
    )
    assert conf
    with open(
        configuration_path.joinpath("example_result.json"), "r", encoding="utf-8"
    ) as expected_result_file:
        expected_result = json.load(expected_result_file)
    TestCase().assertDictEqual(conf, expected_result)


def test_config_with_matching_jsonschema() -> None:
    configuration_path = EXAMPLES_DIR.joinpath("config_with_jsonschema")
    conf = LorenDict(
        configuration_path.joinpath("input_config"),
        lazy=False,
        preserve_file_suffix=False,
    )
    schema_path = configuration_path.joinpath("example_schema.json")
    conf.validate(str(schema_path))

def test_config_with_matching_yamlschema() -> None:
    configuration_path = EXAMPLES_DIR.joinpath("config_with_jsonschema")
    conf = LorenDict(
        configuration_path.joinpath("input_config"),
        lazy=False,
        preserve_file_suffix=False,
    )
    schema_path = configuration_path.joinpath("example_schema.yaml")
    conf.validate(str(schema_path))


def test_config_with_non_matching_jsonschema(tmp_path: Path) -> None:
    configuration_path = EXAMPLES_DIR.joinpath("config_with_jsonschema")
    conf = LorenDict(
        configuration_path.joinpath("input_config"),
        lazy=False,
        preserve_file_suffix=False,
    )
    schema_path = tmp_path.joinpath("wrong_schema.json")
    with open(schema_path, "w+", encoding="utf-8") as schema_file:
        json.dump(
            {
                "$schema": "http://json-schema.org/draft-04/schema#",
                "type": "object",
                "required": ["something_random"],
            },
            schema_file,
        )

    with pytest.raises(ValidationError):
        conf.validate(str(schema_path))


def test_config_with_sub_directories() -> None:
    configuration_path = EXAMPLES_DIR.joinpath("config_with_sub_directories")
    conf = LorenDict(
        configuration_path.joinpath("input_config"),
        lazy=False,
        preserve_file_suffix=False,
    )
    assert conf
    with open(
        configuration_path.joinpath("example_result.json"), "r", encoding="utf-8"
    ) as expected_result_file:
        expected_result = json.load(expected_result_file)

    assert conf == expected_result


def test_template_basic(tmp_path: Path) -> None:
    root_path = EXAMPLES_DIR.joinpath("template_basic")
    conf = LorenDict(
        root_path.joinpath("input_config"),
        lazy=False,
        preserve_file_suffix=False,
    )
    assert conf
    render(
        template_path=str(
            root_path.joinpath("input_template", "basic_template.html.j2")
        ),
        output_path=tmp_path.joinpath("output_file.html"),
        configurations=conf,
        strict=False,
    )
    with open(
        tmp_path.joinpath("output_file.html"), "r", encoding="utf-8"
    ) as result_file, open(
        root_path.joinpath("example_result.html"), "r", encoding="utf-8"
    ) as expected_result_file:
        assert result_file.read() == expected_result_file.read()


def test_template_multiple_files(tmp_path: Path) -> None:
    root_path = EXAMPLES_DIR.joinpath("template_multiple_files")
    conf = LorenDict(
        root_path.joinpath("input_config"), lazy=False, preserve_file_suffix=False
    )
    assert conf
    render(
        template_path=str(root_path.joinpath("input_template", "template.pr")),
        output_path=tmp_path,
        configurations=conf,
        strict=False,
    )
    assert os.listdir(tmp_path) == os.listdir(root_path.joinpath("example_results"))

    for file in os.listdir(tmp_path):
        with open(tmp_path.joinpath(file), "r", encoding="utf-8") as rendered, open(
            root_path.joinpath("example_results", file), "r", encoding="utf-8"
        ) as expected:
            assert rendered.read() == expected.read()


def test_template_airflow_dag(tmp_path: Path) -> None:
    root_path = EXAMPLES_DIR.joinpath("template_airflow_dag")
    conf = LorenDict(
        root_path.joinpath("config"), lazy=False, preserve_file_suffix=False
    )
    assert conf
    render(
        template_path=str(root_path.joinpath("dag_template.py.j2")),
        output_path=tmp_path,
        configurations=conf,
        strict=False,
    )

    def recursive_dict_match(rendered_path: Path, expected_path: Path) -> None:
        assert sorted(os.listdir(rendered_path)) == sorted(os.listdir(expected_path))
        for file in os.listdir(rendered_path):
            if os.path.isdir(rendered_path.joinpath(file)):
                recursive_dict_match(
                    rendered_path.joinpath(file), expected_path.joinpath(file)
                )
            else:
                with open(
                    rendered_path.joinpath(file), "r", encoding="utf-8"
                ) as rendered, open(
                    expected_path.joinpath(file), "r", encoding="utf-8"
                ) as expected:
                    assert sorted(rendered.read().replace("\n", "")) == sorted(
                        expected.read().replace("\n", "")
                    )

    recursive_dict_match(tmp_path, root_path.joinpath("result_dags"))
