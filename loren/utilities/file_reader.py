from typing import Dict


class LorenFileReader:
    @staticmethod
    def read(file_path) -> Dict[str, str]:
        with open(file_path, "rb") as file:
            try:
                return {"file_contents": file.read()}
            except Exception as e:
                print(f"Exception raised when opening {file_path}")
                raise e
