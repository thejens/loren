from loren.load import LorenDict
from pathlib import Path
import pytest
import json

EXAMPLES_DIR = Path(__file__).parent.parent.joinpath("examples")


def test_examples_path():
    assert EXAMPLES_DIR.is_dir()


def test_config_basic():
    configuration_path = EXAMPLES_DIR.joinpath("config_basic")
    conf = LorenDict(
        configuration_path.joinpath("input_config"),
        lazy=False,
        preserve_file_suffix=False,
    ).to_dict()
    assert conf
    with open(
        configuration_path.joinpath("example_result.json"), "r"
    ) as expected_result_file:
        expected_result = json.load(expected_result_file)
    assert conf == expected_result


def test_config_jinja2():
    configuration_path = EXAMPLES_DIR.joinpath("config_with_jinja2")
    conf = LorenDict(
        configuration_path.joinpath("input_config"),
        lazy=False,
        preserve_file_suffix=False,
        additional_args={"parameter_from_call": "test"},
    ).to_dict()
    assert conf
    with open(
        configuration_path.joinpath("example_result.json"), "r"
    ) as expected_result_file:
        expected_result = json.load(expected_result_file)
    assert conf == expected_result

def test_config_with_matching_jsonschema():
    configuration_path = EXAMPLES_DIR.joinpath("config_with_jsonschema")
    conf = LorenDict(
        configuration_path.joinpath("input_config"),
        lazy=False,
        preserve_file_suffix=False
    )
    schema_path = configuration_path.joinpath("example_jsonschema.json")
    conf.validate(schema_path)

def test_config_with_non_matching_jsonschema(tmp_path):
    configuration_path = EXAMPLES_DIR.joinpath("config_with_jsonschema")
    conf = LorenDict(
        configuration_path.joinpath("input_config"),
        lazy=False,
        preserve_file_suffix=False
    )
    schema_path = tmp_path.joinpath("wrong_schema.json")
    with open(schema_path, "w+") as schema_file:
        json.dump({
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "required": [
                "something_random"
            ]
        }, schema_file
        )
    from jsonschema.exceptions import ValidationError
    with pytest.raises(ValidationError):
        conf.validate(schema_path)

