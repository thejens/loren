# Basic Config

Simple example where input is read and then validated using a json schema file, either in JSON or YAML format.

Run with JSON format schema file:
`python -m loren validate --configuration-path examples/config_with_jsonschema/input_config/ --schema-path examples/config_with_jsonschema/example_schema.json`

Run with YAML format schema file:
`python -m loren validate --configuration-path examples/config_with_jsonschema/input_config/ --schema-path examples/config_with_jsonschema/example_schema.yaml`
