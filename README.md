# loren - Load & Render
Loren is a package that treats file-systems as a data structure (FSaaDS anyone?),
and that can translate those into e.g. JSON. Files are scanned recursively and
the contents is put into a nested dict structure based on how they are arranged
in folders.

It also provides the capability to render templates written with Jinja2 using
those data structures as a variable namespace.

The original idea comes from boilerplate-heavy implementations such as
specifying DAG's and tasks in Apache Airflow. Loren proved a powerful tool to
translate the Airflow interface to a configuration structure that were easier
to navigate for a non-technical audience.

However use-cases doesn't end there, you can use a Loren template and
configuration to do things such as "translating a CSV file into one html-file
per row", or genreating a massive single configuration file from a bunch of
specialized config files. (perhaps you want to split the airflow config into
one file per section and have a script that merge the intelligently)

## How it works
Loren will create a `configuration` by parsing all files in a file-tree,
or optionally, a single file. Files are parsed based on their extensions.
For instance a `.yaml` file will be represented as the loaded python
 object in the `configuration`.

If you use Loren as a python module you can parse a file tree into a
 `configuration` by calling the `parse` function in the `parser` module.
  The resulting dict will be returned as is. If you call Loren from the
  command line, you might want to use the `dump` function to dump the
  `configuration` to disk, note that this requires the contents to be
  json serializable.

You can also give Loren a template file, which will be rendered based on
the config using the `render` function in the `renderer` module. The funciton
expects 3 paths as input, where to find the `configuraiton`, where to find the
template file, and where to put the resulting file(s).

The Template is a file that uses Jinja2. If a row in the rendered template
starts with `=> some_file_path/some_file_name` the contents following the
statement will be output to a file named `some_file_name` in a folder named
`some_file_path`. Hence a single template file can render multiple outputs.

If `=>` delimiters are present in the template, the output path argument will
be treateda as a root directory to place files under. If there are no `=>`
delimiters, the output path will be interpreted as a file name.

### Parsing File Types
By default Loren will treat the following extensions:
* `.yaml` & `.yml`: Will be parsed using a Yaml parser and added in its entirety to the `configuration`
* `.json`: Will be parsed using a JSON parser and added in its entirety to the `configuration`
* `.py`: Will be executed and the namespace stored in a dict in the `configuration`
* `.csv` & `.tsv`: Will be parsed and added as a list of dict under the key `rows` in a dict. The first row is used as a header, and `,` or `\t` used as separators for the respective formats.
* Other files are, by default, read as text-files where the contents are added under the key `file_contents`

Some file extensions warrant a special loading process. By default any file name appended with `.j2` or `.jinja2` will be rendered as a jinja2 template before being parsed. To be clear, `some_file.yaml.j2` will be rendered using Jinja2 and then parsed as a yaml file.

`jpg` and `png` are by default read as bytes converted to a base64 representation.

### Brief Example
See the Examples dir for more examples.

Let's say you have the following file structure:
```
|- folder
|----file1.yaml
|----file2.txt
|----sub_folder
|------file3.txt.j2
```
`file1.yaml` contains:
```
foo: bar
```
`file2.txt` contains:
```
Some text
in a text-file
```
`file3.txt.j2` contains:
```
{% set foo="bar" %}A man walks into a {{ foo }}
```
Pointing Loren to create a configuration from `folder` would generate:
```
{
  "file1": {
    "foo": "bar",
    "_path": "files/file1.yaml"
  },
  "file2": {
    "file_contents": "Some text\nin a text-file",
    "_path": "files/file2.txt"
  },
  "sub_folder": {
    "file3": {
      "file_contents": "A man walks into a bar",
      "_path": "files/sub_folder/file3.txt.j2"
    },
  }
}
```

If you use this config path to the render function, and provide a template like
below:
```
=>output_1.htm
<html><body>
<h1>{{ file2._path }}</h1>
<p>{{ file2.file_contents }}</p>
</html></body>
=>output_2.txt
{{ sub_folder.file3.file_contents }}
```
... would generate two files on the output path:
`output_1.htm`:
```
<html><body>
<h1>files/file2.txt</h1>
<p>Some text
in a text-file</p>
</html></body>
```
`output_2.htm`:
```
A man walks into a bar
```

This is a silly example, but given you can use jinja2 conditionals, loops etc.
to generate multiple files based on the configuraiton, it can really become a
swiss army knife for generating complex file structures from simple
configurations.

### Configuring the Configuration
Above shows how files are treated by default, Loren also respects two dotfiles
in the configuration path.

`.lorenignore`
and
`.loren.yaml`

`.lorenignore` works like `.gitignore` and tells Loren to ignore files or
directories when parsing configurations. This is useful for instance when you
want to use some files as jinja2 templates without including the files themselves
in the `configuration`.

`.loren.yaml` specifies two keys, `loaders` and `parsers`, these are references
to what functions to use to load files from disk, and to parse loaded files.

The defaults look like:
```
loaders:
  '*': loren.file_loaders.text_loader.TextLoader
  j2: loren.file_loaders.jinja2_loader.Jinja2Loader
  jinja2: loren.file_loaders.jinja2_loader.Jinja2Loader
  jpg: loren.file_loaders.base64_loader.URLSafeBase64Loader
  png: loren.file_loaders.base64_loader.URLSafeBase64Loader
parsers:
  '*': loren.parsers.text_parser.TextParser
  csv: loren.parsers.csv_parser.CSVParser
  json: loren.parsers.json_parser.JSONParser
  py: loren.parsers.python_parser.PyParser
  tsv: loren.parsers.csv_parser.TSVParser
  yaml: loren.parsers.yaml_parser.YamlParser
  yml: loren.parsers.yaml_parser.YamlParser
```

The keys are file extensions, and the `*` is the default loader to use for
other files. Omiting the `*` will make Loren crash if it comes across a file
it doesn't have support for.

## Install
For now, clone this repo and run:
`python -m pip install -r https://raw.githubusercontent.com/thejens/parender/main/requirements.txt`
`python -m pip install git+https://github.com/thejens/loren.git`

## Run
To run, call `python -m loren COMMAND ARGS` with COMMAND and ARGS as per below.

### Commands & Args
* `render`: Read a configuration folder or file, and render a template
  * `--template-path`: Pointing at a .j2 template file to render
  * `--configuration-path`: Pointing at a `configuration`
  * `--output-path`: Pointing at a folder or file to put output into
* `validate`: Parse a configuration and validate against a jsonschema
  * `--configuration-path`: Pointing at a `configuration`
  * `--schema-path`: Pointing at a jsonschema file
* `print`: Parse a `configuration` and prints it using pprint
  * `--configuration-path`: Pointing at a `configuration`
* `dump`: Parse a `configuration` and dump it as json
  * `--configuration-path`: Pointing at a `configuration`
  * `--output-path`: Path to write json config
* `init`: Sets up a folder to become a new `configuration`, note that the files added by `init` are optional, so you don't have to use this command to create a configuration
  * `--configuration-path`: Pointing at a `configuration`
