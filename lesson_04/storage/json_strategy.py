import json
from pathlib import Path
from lesson_04.storage.abstract import StorageStrategy

files_dir = Path(
    __name__).absolute().parent.parent / "files"
storage_file = "students.json"

class JSONStorageStrategy(StorageStrategy):
    def read(self) -> dict:
        with open(files_dir / storage_file) as file:
            return json.load(file)

    def write(self, data: dict) -> None:
        with open(files_dir / storage_file, mode="w") as file:
            json.dump(data, file)