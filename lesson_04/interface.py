from lesson_04.storage.csv_strategy import CSVStorageStrategy
from lesson_04.storage.json_strategy import JSONStorageStrategy
from lesson_04.storage.txt_strategy import TXTStorageStrategy
from lesson_04.storage.yaml_strategy import YAMLStorageStrategy
from lesson_04.storage.pickle_strategy import PickleStorageStrategy
from lesson_04.storage.students_storage import StudentsStorage
from lesson_04.cruid import search_student, add_marks, student_details, delete_student, update_student, add_student

# strategy = JSONStorageStrategy()
# strategy = YAMLStorageStrategy()
# strategy = PickleStorageStrategy()
# strategy = TXTStorageStrategy()
strategy = CSVStorageStrategy()

def represent_students():
    header = f"{'ID':<5} | {'Name':<20} | {'Marks':<30}"
    separator = "-" * len(header)

    print(header)
    print(separator)

    for id_, student in StudentsStorage(strategy).students.items():
        marks_str = ", ".join(map(str, student['marks']))
        print(f"{id_:<5} | {student['name']:<20} | {marks_str:<30}")

def is_mark(marks):
    try:
        if marks.isdigit():
            mark = [int(marks)]
        else:
            mark = [int(mark.strip()) for mark in marks.split(",")]
        return True
    except ValueError:
        return False

def parse(data: str, action: str):
    items = data.split(";")

    if action == "add":
        template = "John Doe;4,5,4,5,4,5"

        if len(items) != 2:
            raise Exception(f"Incorrect data. Template: {template}")

        # items == ["John Doe", "4,5...."]
        name, raw_marks = items
        try:
            marks = [int(item) for item in raw_marks.split(",")]
        except ValueError as error:
            print(error)
            raise Exception(f"Marks are incorrect. Template: {template}") from error

        return name, marks

    elif action == "update":
        template = "John Doe;4,5,4,5,4,5 or only name: John Doe or only marks: 4,5,4,5,4,5: "

        if 1 < len(items) > 2:
            raise Exception(f"Incorrect data. Template: {template}")

        if len(items) == 2:
            # items == ["John Doe", "4,5...."]
            name, raw_marks = items
            try:
                marks = [int(item) for item in raw_marks.split(",")]
            except ValueError as error:
                print(error)
                raise Exception(f"Marks are incorrect. Template: {template}") from error
            return name, marks

        elif len(items) == 1:
            if not is_mark(items[0]):
                name = str(items[0])

                return name
            else:
                raw_marks = ",".join(map(str, items))
                try:
                    if isinstance(raw_marks, str) and raw_marks.isdigit():
                        marks = [int(raw_marks)]
                    elif isinstance(raw_marks, str):
                        marks = [int(item) for item in raw_marks.split(",")]
                    else:
                        raise ValueError("raw_marks must be a string.")
                except ValueError as error:
                    print(error)
                    raise Exception(f"Marks are incorrect. Template: {template}") from error

                return marks
    elif action == "add_marks":
        template = "1,2,3,4,5"
        raw_marks = ",".join(map(str, items))
        try:
            marks = [int(item) for item in raw_marks.split(",")]
            if any(mark < 1 or mark > 5 for mark in marks):
                raise ValueError(f"All marks must be between 1 and 5. Template: {template}")
        except ValueError as error:
            raise Exception(f"Marks are incorrect or marks must be between 1 and 5. Template: {template}") from error

        return marks

def ask_student_payload(action: str):
    if action == "add":
        prompt = "Enter student's payload using next template:\n'John Doe;4,5,4,5,4,5': "

        if not (payload := parse(input(prompt), action)):
            return None
        else:
            name, marks = payload

        return {"name": name, "marks": marks}

    elif action == "update":
        prompt = "Enter student's payload using next template:\n'John Doe;4,5,4,5,4,5' or only name: John Doe or only marks: 4,5,4,5,4,5: "

        if not (payload := parse(input(prompt), action)):
            return None
        else:
            while True:
                if isinstance(payload, tuple):
                    name, marks = payload
                    data = {"name": name, "marks": marks}
                elif isinstance(payload, (list, str)):
                    data = payload
                else:
                    return None

                confirm = input(
                    f"Are you sure you want to change student's data to {data}? (y/n): ")
                if confirm == 'y':
                    return data
                elif confirm == 'n':
                    print(f"❌ Changing data has been canceled by the user.")
                    return None
                else:
                    print("Invalid input, please try again. Enter 'y' or 'n'.")
    elif action == "add_marks":
        prompt = "Enter the marks to add (integer between 1 and 5) using next template 1,2,3,4,5:"

        if not (payload := parse(input(prompt), action)):
            return None
        else:
            while True:
                confirm = input(
                    f"Are you sure you want to change student's data to {payload}? (y/n): ")
                if confirm == 'y':
                    marks = payload
                    return marks
                elif confirm == 'n':
                    print(f"❌ Changing data has been canceled by the user.")
                    return None
                else:
                    print("Invalid input, please try again. Enter 'y' or 'n'.")

def handle_management_command(command: str):
    if command == "show":
        represent_students()

    elif command == "add marks":
        represent_students()
        add_marks_id = input("Enter student's id you wanna add marks: ")

        try:
            id_ = int(add_marks_id)
            if not search_student(id_):
                raise KeyError(f"Student with id {add_marks_id} does not exist.")
        except ValueError as error:
            raise Exception(f"ID '{add_marks_id}' is not correct value") from error
        else:
            if data := ask_student_payload("add_marks"):
                add_marks(id_, data)
                print(f"✅ Marks are added")
                if student := search_student(id_):
                    student_details(student)
                else:
                    print(f"❌ Can not change user with data {data}")

    elif command == "retrieve":
        search_id = input("Enter student's id to retrieve: ")

        try:
            id_ = int(search_id)
        except ValueError as error:
            raise Exception(f"ID '{search_id}' is not correct value") from error
        else:
            if student := search_student(id_):
                student_details(student)
            else:
                print(f"There is not student with id: '{id_}'")

    elif command == "remove":
        delete_id = input("Enter student's id to remove: ")

        try:
            id_ = int(delete_id)
        except ValueError as error:
            raise Exception(f"ID '{delete_id}' is not correct value") from error
        else:
            delete_student(id_)

    elif command == "change":
        represent_students()
        update_id = input("Enter student's id you wanna change: ")

        try:
            id_ = int(update_id)
            if not search_student(id_):
                raise KeyError(f"Student with id {update_id} does not exist.")
        except ValueError as error:
            raise Exception(f"ID '{update_id}' is not correct value") from error
        else:
            if data := ask_student_payload("update"):

                update_student(id_, data)
                print(f"✅ Student is updated")
                if student := search_student(id_):
                    student_details(student)
                else:
                    print(f"❌ Can not change user with data {data}")

    elif command == "add":
        data = ask_student_payload("add")
        if data is None:
            return None
        else:
            if not (student := add_student(data)):
                print(f"❌ Can't create user with data: {data}")
            else:
                print(f"✅ New student '{student['name']}' is created")
    else:
        raise SystemExit(f"Unrecognized command: '{command}'")

def handle_user_input():
    """This is an application entrypoint."""

    SYSTEM_COMMANDS = ("quit", "help")
    MANAGEMENT_COMMANDS = ("show", "add", "retrieve", "remove", "change", "add marks")
    AVAILABLE_COMMANDS = SYSTEM_COMMANDS + MANAGEMENT_COMMANDS

    help_message = (
        "Welcome to the Journal application. Use the menu to interact with the application.\n"
        f"Available commands: {AVAILABLE_COMMANDS}"
    )

    print(help_message)

    while True:
        command = input("Enter the command: ")

        if command == "quit":
            print(f"\nThanks for using Journal application. Bye!")
            break
        elif command == "help":
            print(help_message)
        elif command in MANAGEMENT_COMMANDS:
            try:
                handle_management_command(command=command)
            except Exception as error:
                print(f"Error: {error}")
        else:
            print(f"Unrecognized command '{command}'")