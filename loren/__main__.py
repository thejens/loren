# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import os
from typing import Any, List, Dict, Union
from argparse import ArgumentParser
from os.path import dirname
from pathlib import Path
import json
from loren.load import LorenDict
from loren.render import render
from loren.utilities.configuration import LorenConfiguration


def _parse_configuration_path(
    configuration_path: List[str],
) -> Union[Path, List[Path], Dict[str, Path]]:
    if isinstance(configuration_path[0], List):
        configuration_path = [
            item for sublist in configuration_path for item in sublist
        ]

    if ":" in configuration_path[0]:
        path_dict = {}
        for item in configuration_path:
            key, path = item.split(":")
            path_dict[key] = Path(path)
        return path_dict

    elif len(configuration_path) == 1:
        return Path(configuration_path[0])

    return [Path(p) for p in configuration_path]


def _parse_template_path(template_path: List[str]) -> Any:
    if isinstance(template_path[0], List):
        template_path = [item for sublist in template_path for item in sublist]

    return template_path


def action_render() -> None:
    parser = ArgumentParser(
        description="Render a set of files based on a template and conf"
    )
    parser.add_argument(
        "--template-path", "-t", type=str, required=True, action="append"
    )
    parser.add_argument(
        "--configuration-path",
        "-c",
        nargs="+",
        type=str,
        required=True,
        action="append",
    )
    parser.add_argument("--output-path", "-o", type=str, default="rendered")
    parser.add_argument("--schema-path", "-s", type=str, default=None)
    parser.add_argument("--strict", default=False, action="store_true")
    parser.add_argument("--dry-run", default=False, action="store_true")
    args, unknown_args = parser.parse_known_args()
    packaged_unknown_args = package_unknown_args(unknown_args)

    configurations = LorenDict(
        path=_parse_configuration_path(args.configuration_path),
        additional_args=packaged_unknown_args,
        lazy=False,
    )
    if args.schema_path:
        configurations.validate(args.schema_path)

    template_paths = _parse_template_path(args.template_path)
    for template_path in template_paths:
        render(
            template_path=template_path,
            output_path=args.output_path,
            configurations=configurations,
            strict=args.strict,
            dry_run=args.dry_run,
            **packaged_unknown_args
        )


def action_validate() -> None:
    parser = ArgumentParser(
        description="Validate a configuration result using jsonschema"
    )
    parser.add_argument(
        "--configuration-path", "-c", nargs="+", type=str, required=True
    )
    parser.add_argument("--schema-path", "-s", type=str, required=True)
    args, unknown_args = parser.parse_known_args()
    packaged_unknown_args = package_unknown_args(unknown_args)

    LorenDict(
        path=_parse_configuration_path(args.configuration_path),
        lazy=False,
        additional_args=packaged_unknown_args,
    ).validate(args.schema_path)
    print("Configuration is valid")


def action_print() -> None:
    parser = ArgumentParser(description="Print a parsed configuration")
    parser.add_argument(
        "--configuration-path", "-c", nargs="+", type=str, required=True
    )
    args, unknown_args = parser.parse_known_args()
    packaged_unknown_args = package_unknown_args(unknown_args)
    print(
        json.dumps(
            LorenDict(
                path=_parse_configuration_path(args.configuration_path),
                lazy=False,
                additional_args=packaged_unknown_args,
            ),
            indent=4,
            sort_keys=True,
        )
    )


def action_dump() -> None:
    parser = ArgumentParser(description="Print a parsed configuration")
    parser.add_argument(
        "--configuration-path", "-c", nargs="+", type=str, required=True
    )
    parser.add_argument("--output-path", "-o", type=str, required=True)
    args, unknown_args = parser.parse_known_args()
    packaged_unknown_args = package_unknown_args(unknown_args)

    if dirname(args.output_path):
        os.makedirs(dirname(args.output_path), exist_ok=True)
    with open(args.output_path, "w+", encoding="utf-8") as file:
        json.dump(
            LorenDict(
                path=_parse_configuration_path(args.configuration_path),
                additional_args=packaged_unknown_args,
                lazy=False,
            ),
            file,
        )


def action_init() -> None:
    parser = ArgumentParser(description="Print a parsed configuration")
    parser.add_argument(
        "--configuration-path",
        "-c",
        nargs="+",
        type=str,
        required=True,
        action="append",
    )
    args, _ = parser.parse_known_args()
    if isinstance(args.configuration_path[0], List):
        directories = [
            Path(item.split(":")[-1])
            for sublist in args.configuration_path
            for item in sublist
        ]
    else:
        directories = [Path(item.split(":")[-1]) for item in args.configuration_path]

    for path in directories:
        LorenConfiguration.create_default_configuration(path)


def package_unknown_args(arglist: list) -> dict:
    if not arglist:
        return {}
    arglist.pop(0)
    new_args: dict = {}
    key = "positional_args"
    for arg in arglist:
        if arg[0] == "-":
            key = arg.strip("-").replace("-", "_")
        else:
            if key in new_args:
                if not isinstance(new_args[key], List):
                    new_args[key] = [new_args[key], arg]
                else:
                    new_args[key].append(arg)
            else:
                new_args[key] = arg
    return new_args


if __name__ == "__main__":

    action_parser = ArgumentParser(
        description="Parse file trees to config, generate files from configs"
        + "\n\nSupply One of [render, validate, print, dump, init]"
        + "\n as first argument"
    )
    action_parser.add_argument("action", type=str)
    action = action_parser.parse_known_args()[0].action

    if action == "render":
        action_render()

    elif action == "validate":
        action_validate()

    elif action == "print":
        action_print()

    elif action == "dump":
        action_dump()

    elif action == "init":
        action_init()

    else:
        action_parser.print_help()
