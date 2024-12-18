"""
Student:
    name: str
    marks: list[int]

Features:
- fetch all students from the database
- add another yet student to the database
- retrieve the student by NAME. UI/UX issues...
"""

# ==================================================
# Simulated storage
# ==================================================
students = {
    1: {
        "name": "John Doe",
        "marks": [4, 5, 1, 4, 5, 2, 5],
        "info": "John is 22 y.o. Hobbies: music",
    },
    2: {
        "name": "Marry Black",
        "marks": [4, 1, 3, 4, 5, 1, 2, 2],
        "info": "John is 23 y.o. Hobbies: football",
    },
}

LAST_ID_CONTEXT = 2


def represent_students():
    header = f"{'ID':<5} | {'Name':<20} | {'Marks':<30}"
    separator = "-" * len(header)

    print(header)
    print(separator)

    for id_, student in students.items():
        marks_str = ", ".join(map(str, student['marks']))
        print(f"{id_:<5} | {student['name']:<20} | {marks_str:<30}")


# ==================================================
# CRUD (Create Read Update Delete)
# ==================================================
def add_student(student: dict) -> dict | None:
    global LAST_ID_CONTEXT

    if len(student) != 2:
        return None
    elif not student.get("name") or not student.get("marks"):
        return None
    else:
        LAST_ID_CONTEXT += 1
        students[LAST_ID_CONTEXT] = student

    return student


def search_student(id_: int) -> dict | None:
    return students.get(id_)


def delete_student(id_: int):
    if search_student(id_):
        del students[id_]
        print(f"Student with id '{id_}' is deleted")
    else:
        print(f"There is student '{id_}' in the storage")


def update_student(id_: int, payload: dict | str | list | int) -> dict:
    if id_ not in students:
        raise KeyError(f"Student with ID {id_} does not exist.")
    if isinstance(payload, dict):
        students[id_] = payload
    elif isinstance(payload, str):
        students[id_]["name"] = payload
    elif isinstance(payload, list):
        students[id_]["marks"] = payload
    else:
        raise TypeError("Payload must be a dict, string, or list.")

    return students[id_]


def add_marks(id_: int, new_marks: list[int]):
    if id_ not in students:
        raise KeyError(f"Student with ID {id_} does not exist.")
    students[id_]["marks"].extend(new_marks)

    return students[id_]


def student_details(student: dict) -> None:
    print(f"Detailed info: [{student['name']}, {student['marks']}]")


# ==================================================
# Handle user input
# ==================================================
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


def is_mark(marks):
    try:
        if marks.isdigit():
            mark = [int(marks)]
        else:
            mark = [int(mark.strip()) for mark in marks.split(",")]
        return True
    except ValueError:
        return False


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
            if isinstance(payload, tuple):
                name, marks = payload
                return {"name": name, "marks": marks}
            elif isinstance(payload, list):
                marks = payload
                return marks
            elif isinstance(payload, str):
                name = payload
                return name
    elif action == "add_marks":
        prompt = "Enter the marks to add (integer between 1 and 5) using next template 1,2,3,4,5:"

        if not (payload := parse(input(prompt), action)):
            return None
        else:
            marks = payload
            return marks


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
                while True:
                    confirm = input(
                        f"Are you sure you want to add these marks {data} to student with id {id_}? (y/n): ")
                    if confirm == 'y':
                        add_marks(id_, data)
                        print(f"✅ Marks are added")
                        if student := search_student(id_):
                            student_details(student)
                            break
                        else:
                            print(f"❌ Can not change user with data {data}")
                            break
                    elif confirm == 'n':
                        print(f"❌ Adding marks has been canceled by the user.")
                        break
                    else:
                        print("Invalid input, please try again. Enter 'yes' or 'no'.")

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
                while True:
                    confirm = input(
                        f"Are you sure you want to change these student's data {data} with id {id_}? (y/n): ")
                    if confirm == 'y':
                        update_student(id_, data)
                        print(f"✅ Student is updated")
                        if student := search_student(id_):
                            student_details(student)
                            break
                        else:
                            print(f"❌ Can not change user with data {data}")
                            break
                    elif confirm == 'n':
                        print(f"❌ Changing data has been canceled by the user.")
                        break
                    else:
                        print("Invalid input, please try again. Enter 'yes' or 'no'.")

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


handle_user_input()
