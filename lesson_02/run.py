COMMANDS = ("quit", "show", "retrieve by name", "retrieve by id", "add")

student_id: int = 0
# Simulated database
students = [
    {
        "id": 1,
        "name": "John Doe",
        "marks": [4, 5, 1, 4, 5, 2, 5],
        "info": "John is 22 y.o. Hobbies: music",
    },
    {
        "id": 2,
        "name": "Marry Black",
        "marks": [4, 1, 3, 4, 5, 1, 2, 2],
        "info": "John is 23 y.o. Hobbies: football",
    },
]
student_id += len(students)


def find_student_by_name(name: str) -> dict | None:
    for student in students:
        if student["name"] == name:
            return student

    return None


def find_student_by_id(students_id: int) -> dict | None:
    for student in students:
        if student["id"] == students_id:
            return student

    return None


def show_students() -> None:
    print("=" * 20)
    print("The list of students:\n")
    for student in students:
        print(f"Id: {student['id']}. Name: {student['name']}. Marks: {student['marks']}")

    print("=" * 20)


def show_student_by_name(name: str) -> None:
    student: dict | None = find_student_by_name(name)

    if not student:
        print(f"There is no student {name}")
        return

    print("Detailed about student:\n")
    print(
        f"Id: {student['id']}. Name: {student['name']}. Marks: {student['marks']}\n"
        f"Details: {student['info']}\n"
    )


def show_student_by_id(students_id: int) -> None:
    student: dict | None = find_student_by_id(students_id)

    if not student:
        print(f"There is no student with id {students_id}")
        return

    print("Detailed about student:\n")
    print(
        f"Id: {student['id']}. Name: {student['name']}. Marks: {student['marks']}\n"
        f"Details: {student['info']}\n"
    )


def add_student(student_name: str, student_details: str | None):
    global student_id
    student_id += 1
    instance = {
        "id": student_id,
        "name": student_name,
        "marks": [],
        "info": student_details if student_details else None}
    students.append(instance)

    return instance


def main():
    print(f"Welcome to the Digital journal!\nAvailable commands: {COMMANDS}")
    while True:
        user_input = input("Enter the command: ")

        if user_input not in COMMANDS:
            print(f"Command {user_input} is not available.\n")
            continue

        if user_input == "quit":
            print("See you next time.")
            break

        try:
            if user_input == "show":
                show_students()
            elif user_input == "retrieve by name":
                student_name = input("Enter student name you are looking for: ")
                show_student_by_name(student_name)
            elif user_input == "retrieve by id":
                while True:
                    student_id_int = input("Enter student id you are looking for: ").strip()
                    if not student_id_int.isdigit():
                        print("Invalid id format or field is empty. Please try again")
                    else:
                        break
                int_student_id = int(student_id_int)
                show_student_by_id(int_student_id)
            elif user_input == "add":
                while True:
                    name = input("Enter student's name: ").strip()
                    if not name:
                        print("Name cannot be empty. Please try again.")
                    else:
                        break
                details = input("Enter student's details (optional): ")
                add_student(name, details if details else None)
        except NotImplementedError as error:
            print(f"Feature '{error}' is not ready for live.")
        except Exception as error:
            print(error)


main()
