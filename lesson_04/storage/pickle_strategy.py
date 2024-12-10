from pathlib import Path
import pickle
from lesson_04.storage.abstract import StorageStrategy

# ==================================================
# Simulated storage
# ==================================================
files_dir = Path(
    __name__).absolute().parent.parent / "files"
pickle_storage_file = "students.pkl"

class PickleStorageStrategy(StorageStrategy):
    def read(self) -> dict:
        with open(files_dir / pickle_storage_file, mode="rb") as file:
            return pickle.load(file)

    def write(self, data: dict) -> None:
        with open(files_dir / pickle_storage_file, mode="wb") as file:
            pickle.dump(data, file)




