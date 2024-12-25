import csv
from pathlib import Path
from lesson_04.storage.abstract import StorageStrategy

files_dir = Path(
    __name__).absolute().parent.parent / "files"
csv_storage_file = "students.csv"

class CSVStorageStrategy(StorageStrategy):
    def read(self) -> dict:
        students = {}
        last_id_context = 0
        with open(files_dir / csv_storage_file) as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["id"] == "LAST_ID_CONTEXT":
                    last_id_context = int(row["name"])
                else:
                    student_id = row["id"]
                    students[student_id] = {
                        "name": row["name"],
                        "marks": [int(mark) for mark in row["marks"].split(";")],
                        "info": row.get("info", "")
                    }
        return {"students": students, "LAST_ID_CONTEXT": last_id_context}

    def write(self, data: dict) -> None:
        with open(files_dir / csv_storage_file, mode="w") as file:
            fieldnames = ["id", "name", "marks", "info"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for student_id, student in data["students"].items():
                writer.writerow({
                    "id": student_id,
                    "name": student["name"],
                    "marks": ";".join(str(mark) for mark in student["marks"]),
                    "info": student.get("info", "")
                })
            writer.writerow({
                "id": "LAST_ID_CONTEXT",
                "name": str(data["LAST_ID_CONTEXT"]),
                "marks": "",
                "info": ""
            })