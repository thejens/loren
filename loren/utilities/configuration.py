import yaml
import os
import pathspec

DEFAULT_CONFIG = {
    "file_handlers": {
        "yaml": "loren.parsers.yaml_parser.YamlParser",
        "yml": "loren.parsers.yaml_parser.YamlParser",
        "json": "loren.parsers.json_parser.JSONParser",
        "py": "loren.parsers.python_parser.PyParser",
        "csv": "loren.parsers.csv_parser.CSVParser",
        "tsv": "loren.parsers.csv_parser.TSVParser",
        "j2": "loren.parsers.jinja2_parser.Jinja2Parser",
        "jinja2": "loren.parsers.jinja2_parser.Jinja2Parser",
        "*": "loren.parsers.text_parser.TextParser",
    },
    "ignore": [
        ".loren.yml",
        ".DS_Store",
        "_*",
        ".*",
    ],
}


def init_configuration(path):
    with open(path, "w+") as file:
        yaml.dump(DEFAULT_CONFIG, file)


def get_configuration(path):
    try:
        with open(os.path.join(path, ".loren.yml"), "r") as f:
            config = yaml.safe_load(f)
    except (FileNotFoundError, NotADirectoryError):
        config = DEFAULT_CONFIG

    config["ignore"] = pathspec.PathSpec.from_lines(
        "gitwildmatch", config.get("ignore", [])
    )
    config["base_path"] = path
    return config
