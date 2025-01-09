from pathlib import Path
from lesson_04.storage.abstract import StorageStrategy


files_dir = Path(
    __name__).absolute().parent.parent / "files"
txt_storage_file = "students.txt"

class TXTStorageStrategy(StorageStrategy):
    def read(self) -> dict:
        students = {}
        last_id_context = 0
        with open(files_dir / txt_storage_file) as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("LAST_ID_CONTEXT"):
                    last_id_context = int(line.split(":")[1].strip())
                else:
                    parts = line.strip().split(",")
                    student_id = parts[0]
                    students[student_id] = {
                        "name": parts[1],
                        "marks": [int(mark) for mark in parts[2].split(";")],
                        "info": parts[3] if len(parts) > 3 else ""
                    }
        return {"students": students, "LAST_ID_CONTEXT": last_id_context}

    def write(self, data: dict) -> None:
        with open(files_dir / txt_storage_file, mode="w") as file:
            for student_id, student in data["students"].items():
                file.write(f"{student_id},{student['name']},{';'.join(str(mark) for mark in student['marks'])},{student.get('info', '')}\n")
            file.write(f"LAST_ID_CONTEXT:{data['LAST_ID_CONTEXT']}\n")