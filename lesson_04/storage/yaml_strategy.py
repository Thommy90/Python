import yaml #pip install pyyaml
from pathlib import Path
from lesson_04.storage.abstract import StorageStrategy

files_dir = Path(
    __name__).absolute().parent.parent / "files"
yaml_storage_file = "students.yaml"

class YAMLStorageStrategy(StorageStrategy):
    def read(self) -> dict:
        with open(files_dir / yaml_storage_file) as file:
            return yaml.safe_load(file)

    def write(self, data: dict) -> None:
        with open(files_dir / yaml_storage_file, mode="w") as file:
            yaml.safe_dump(data, file)