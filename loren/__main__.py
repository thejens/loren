import json
import os
from pprint import pprint
from argparse import ArgumentParser
from loren.load import LorenDict
from loren.render import render
from loren.utilities.configuration import init_configuration
from os.path import dirname


def action_render():
    parser = ArgumentParser(
        description="Render a set of files based on a template and conf"
    )
    parser.add_argument("--template-path", type=str, required=True)
    parser.add_argument("--configuration-path", type=str, required=True)
    parser.add_argument("--output-path", type=str, default="rendered")
    parser.add_argument("--schema-path", type=str, default=None)
    parser.add_argument("--strict", default=False, action="store_true")
    args, unknown_args = parser.parse_known_args()
    unknown_args = package_unknown_args(unknown_args)

    configurations = LorenDict(args.configuration_path, additional_args=unknown_args)
    if args.schema_path:
        configurations.validate(args.schema_path)

    render(
        template_path=args.template_path,
        output_path=args.output_path,
        configurations=LorenDict,
        strict=args.strict,
        **unknown_args
    )


def action_validate():
    parser = ArgumentParser(
        description="Validate a configuration result using jsonschema"
    )
    parser.add_argument("--configuration-path", type=str, required=True)
    parser.add_argument("--schema-path", type=str, required=True)
    args, unknown_args = parser.parse_known_args()
    unknown_args = package_unknown_args(unknown_args)
    if args.schema_path:
        LorenDict(args.configuration_path, additional_args=unknown_args).validate(
            args.schema_path
        )


def action_print():
    parser = ArgumentParser(description="Print a parsed configuration")
    parser.add_argument("--configuration-path", type=str, required=True)
    args, unknown_args = parser.parse_known_args()
    unknown_args = package_unknown_args(unknown_args)
    pprint(LorenDict(args.configuration_path, additional_args=unknown_args).to_dict())


def action_dump():
    parser = ArgumentParser(description="Print a parsed configuration")
    parser.add_argument("--configuration-path", type=str, required=True)
    parser.add_argument("--output-path", type=str, required=True)
    args, unknown_args = parser.parse_known_args()
    unknown_args = package_unknown_args(unknown_args)
    if dirname(args.output_path):
        os.makedirs(dirname(args.output_path), exist_ok=True)
    with open(args.output_path, "w+") as f:
        json.dump(
            LorenDict(
                args.configuration_path, additional_args=unknown_args, lazy=False
            ),
            f,
        )


def action_init():
    parser = ArgumentParser(description="Print a parsed configuration")
    parser.add_argument("--configuration-path", type=str, required=True)
    args, _ = parser.parse_known_args()
    init_configuration(args.configuration_path)


def package_unknown_args(arglist):
    arglist.pop(0)
    new_args = {}
    key = "positional_args"
    for arg in arglist:
        if arg[0] == "-":
            key = arg.strip("-").replace("-", "_")
        else:
            if key in new_args:
                if type(new_args[key]) is not list:
                    new_args[key] = [new_args[key], arg]
                else:
                    new_args[key].append(arg)
            else:
                new_args[key] = arg
    return new_args


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Parse file trees to config, generate files from configs"
        + "\n\nSupply One of [render, validate, print, dump, init]"
        + "\n as first argument"
    )
    parser.add_argument("action", type=str)
    action = parser.parse_known_args()[0].action

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
        parser.print_help()
