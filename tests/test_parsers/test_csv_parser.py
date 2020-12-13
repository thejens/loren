from parender.parsers.base_parser import BaseParser
from parender.parsers.csv_parser import CSVParser, TSVParser

csv_data = """a,b,c\n1,2,3\n4,5,6\na,"b,c",d"""


def test_class():
    assert issubclass(CSVParser, BaseParser)
    assert issubclass(TSVParser, BaseParser)


def test_csv_parser():
    assert CSVParser.parse(csv_data) == {
      "rows": [
        {"a": "1", "b": "2", "c": "3"},
        {"a": "4", "b": "5", "c": "6"},
        {"a": "a", "b": "b,c", "c": "d"},
      ]
    }


def test_tsv_parser():
    assert TSVParser.parse(csv_data.replace(",", "\t")) == {
      "rows": [
        {"a": "1", "b": "2", "c": "3"},
        {"a": "4", "b": "5", "c": "6"},
        {"a": "a", "b": "b\tc", "c": "d"},
      ]
    }
