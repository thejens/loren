import json
import os
from pprint import pprint
from argparse import ArgumentParser
from parender import parse, validate, render, init
from os.path import dirname


def action_render():
    parser = ArgumentParser(
        description='Render a set of files based on a template and conf'
    )
    parser.add_argument('--template-path', type=str, required=True)
    parser.add_argument('--configuration-path', type=str, required=True)
    parser.add_argument('--render-path', type=str, default="rendered")
    args, unknown_args = parser.parse_known_args()
    unknown_args = package_unknown_args(unknown_args)

    render(
        template_path=args.template_path,
        render_path=args.render_path,
        configurations=parse(args.configuration_path, **unknown_args),
        **unknown_args
    )


def action_validate():
    parser = ArgumentParser(
        description='Validate a configuration result using jsonschema'
    )
    parser.add_argument('--configuration-path', type=str, required=True)
    parser.add_argument('--schema-path', type=str, required=True)
    args, unknown_args = parser.parse_known_args()
    unknown_args = package_unknown_args(unknown_args)
    validate(
        configurations=parse(args.configuration_path, **unknown_args),
        schema_path=args.schema_path
    )


def action_print():
    parser = ArgumentParser(
        description='Print a parsed configuration'
    )
    parser.add_argument('--configuration-path', type=str, required=True)
    args, unknown_args = parser.parse_known_args()
    unknown_args = package_unknown_args(unknown_args)
    pprint(parse(args.configuration_path, **unknown_args))


def action_dump():
    parser = ArgumentParser(
        description='Print a parsed configuration'
    )
    parser.add_argument('--configuration-path', type=str, required=True)
    parser.add_argument('--output-path', type=str, required=True)
    args, unknown_args = parser.parse_known_args()
    unknown_args = package_unknown_args(unknown_args)
    os.makedirs(dirname(args.output_path), exist_ok=True)
    with open(args.output_path, "w+") as f:
        json.dump(parse(args.configuration_path, **unknown_args), f)


def action_init():
    parser = ArgumentParser(
        description='Print a parsed configuration'
    )
    parser.add_argument('--configuration-path', type=str, required=True)
    args, _ = parser.parse_known_args()
    init(args.configuration_path)


def package_unknown_args(arglist):
    arglist.pop(0)
    new_args = {}
    key = "positional_args"
    for arg in arglist:
        if arg[0] == "-":
            key = arg.strip("-")
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
        description='Parse file trees to config, generate files from configs'
    )
    parser.add_argument('action', type=str)
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
