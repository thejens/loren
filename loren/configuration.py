import yaml

DEFAULT_CONFIG = {
    "file_handlers": {
        "yaml": "parsers.yaml_parser.YamlParser",
        "yml": "parsers.yaml_parser.YamlParser",
        "json": "parsers.json_parser.JSONParser",
        "py": "parsers.python_parser.PyParser",
        "csv": "parsers.csv_parser.CSVParser",
        "tsv": "parsers.csv_parser.TSVParser",
        "j2": "parsers.jinja2_parser.Jinja2Parser",
        "jinja2": "parsers.jinja2_parser.Jinja2Parser",
        "jpg": "file_loaders.base64_loader.URLSafeBase64Loader",
        "png": "file_loaders.base64_loader.URLSafeBase64Loader",
        "*": "file_loaders.text_loader.TextLoader",
        "*": "parsers.text_parser.TextParser",
    },
    "ignore": [
        ".loren.yml",
        ".DS_Store",
        "_*",
        ".*",
        "folder_b/"
    ]
}

def init_configuration(path):
    with open(path, "w+") as file:
        yaml.dump(DEFAULT_CONFIG, file)