# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from pathlib import Path
from loren.parsers.base_parser import BaseParser
from loren.parsers.jinja2_parser import Jinja2Parser


def test_class() -> None:
    assert issubclass(Jinja2Parser, BaseParser)


def test_jinja2_parser_basic() -> None:
    assert Jinja2Parser.parse(
        {"file_contents": "This is a {{ 'test' }}"}, root_path="", additional_args={}
    ) == {"file_contents": "This is a test"}


def test_jinja2_parser_no_additional_args() -> None:
    assert Jinja2Parser.parse(
        {"file_contents": "This is a {{ 'test' }}"}, root_path="", additional_args=None
    ) == {"file_contents": "This is a test"}


def test_jinja2_parser_additional_args() -> None:
    assert (
        Jinja2Parser.parse(
            {"file_contents": "This is a {{ some_arg }}"},
            root_path="",
            additional_args={"some_arg": "test"},
        )
        == {"file_contents": "This is a test"}
    )


def test_jinja2_parser_additional_macro(tmp_path: Path) -> None:
    with open(f"{tmp_path}/macro.j2", "w+", encoding="utf-8") as templated_file:
        templated_file.write("{% set foo = 'bar' %}")

    assert (
        Jinja2Parser.parse(
            {"file_contents": "{% import 'macro.j2' as m %}{{ m.foo }}"},
            root_path=tmp_path,
            additional_args={},
        )
        == {"file_contents": "bar"}
    )
