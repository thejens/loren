class LorenFileReader:
    @staticmethod
    def read(file_path) -> str:
        with open(file_path, "rb") as file:
            try:
                return file.read()
            except Exception as e:
                print(f"Exception raised when opening {file_path}")
                raise e
