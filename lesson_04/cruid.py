from lesson_04.storage.csv_strategy import CSVStorageStrategy
from lesson_04.storage.json_strategy import JSONStorageStrategy
from lesson_04.storage.txt_strategy import TXTStorageStrategy
from lesson_04.storage.yaml_strategy import YAMLStorageStrategy
from lesson_04.storage.pickle_strategy import PickleStorageStrategy
from lesson_04.storage.students_storage import StudentsStorage

# strategy = JSONStorageStrategy()
# strategy = YAMLStorageStrategy()
# strategy = PickleStorageStrategy()
# strategy = TXTStorageStrategy()
strategy = CSVStorageStrategy()

# ==================================================
# CRUD (Create Read Update Delete)
# ==================================================
def add_student(student: dict) -> dict | None:
    storage = StudentsStorage(strategy)

    if len(student) != 2:
        return None
    elif not student.get("name") or not student.get("marks"):
        return None
    else:
        storage.last_id_context += 1
        storage.students[str(storage.last_id_context)] = student

    storage.flush()
    return student


def search_student(id_: int) -> dict | None:
    storage = StudentsStorage(strategy)
    return storage.students.get(str(id_))


def delete_student(id_: int):
    storage = StudentsStorage(strategy)

    if search_student(id_):
        del storage.students[str(id_)]
        storage.flush()
        print(f"Student with id '{id_}' is deleted")
    else:
        print(f"There is student '{id_}' in the storage")


def update_student(id_: int, payload: dict | str | list | int) -> dict:
    storage = StudentsStorage(strategy)

    if str(id_) not in storage.students:
        raise KeyError(f"Student with ID {str(id_)} does not exist.")
    if isinstance(payload, dict):
        storage.students[str(id_)] = payload
        storage.flush()
    elif isinstance(payload, str):
        storage.students[str(id_)]["name"] = payload
        storage.flush()
    elif isinstance(payload, list):
        storage.students[str(id_)]["marks"] = payload
        storage.flush()
    else:
        raise TypeError("Payload must be a dict, string, or list.")

    return storage.students[str(id_)]


def add_marks(id_: int, new_marks: list[int]):
    storage = StudentsStorage(strategy)

    if str(id_) not in storage.students:
        raise KeyError(f"Student with ID {str(id_)} does not exist.")
    storage.students[str(id_)]["marks"].extend(new_marks)
    storage.flush()
    return storage.students[str(id_)]


def student_details(student: dict) -> None:
    print(f"Detailed info: [{student['name']}, {student['marks']}]")