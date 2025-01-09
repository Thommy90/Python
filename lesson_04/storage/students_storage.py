from lesson_04.storage.abstract import StorageStrategy

class StudentsStorage:
    def __init__(self, strategy: StorageStrategy) -> None:
        self.strategy = strategy
        data = self.strategy.read()
        self.students = data.get("students", {})
        self.last_id_context = data.get("LAST_ID_CONTEXT", 0)

    def flush(self) -> None:
        data = {
            "students": self.students,
            "LAST_ID_CONTEXT": self.last_id_context
        }
        self.strategy.write(data)