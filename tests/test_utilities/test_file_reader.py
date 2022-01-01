from loren.utilities.file_reader import LorenFileReader


def test_file_reader(tmp_path):
    with open(f"{tmp_path}/.some_file.yml", "w+") as raw_file:
        raw_file.write("some test text")

    assert LorenFileReader.read(f"{tmp_path}/.some_file.yml") == {
        "file_contents": "some test text".encode("utf-8")
    }
