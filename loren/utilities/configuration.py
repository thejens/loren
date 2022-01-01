import yaml
import os
import pathspec

CONFIG_FILE_NAME = ".loren.yml"
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
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, CONFIG_FILE_NAME), "w+") as file:
        yaml.dump(DEFAULT_CONFIG, file)


def get_configuration(path):
    try:
        with open(os.path.join(path, CONFIG_FILE_NAME), "r") as f:
            config = yaml.safe_load(f)
            if "file_handlers" not in config:
                config["file_handlers"] = DEFAULT_CONFIG["file_handlers"].copy()
            if "ignore" not in config:
                config["ignore"] = []

    except (FileNotFoundError, NotADirectoryError):
        config = DEFAULT_CONFIG.copy()

    config["ignore_paths"] = pathspec.PathSpec.from_lines(
        "gitwildmatch", config["ignore"]
    )
    config["base_path"] = path
    return config
