class DatabaseError(Exception):
    """Базовый класс для всех ошибок базы данных."""
    pass


class TableNotFoundError(DatabaseError, KeyError):
    def __init__(self, table_name: str):
        self.table_name = table_name
        super().__init__(f"Ошибка: таблицы '{table_name}' не существует.")


class TableExistsError(DatabaseError, ValueError):
    def __init__(self, table_name: str):
        self.table_name = table_name
        super().__init__(f"Ошибка: таблица '{table_name}' уже существует.")


class ColumnCountError(DatabaseError, ValueError):
    def __init__(self, expected: int, actual: int):
        self.expected = expected
        self.actual = actual
        super().__init__("Ошибка: неверное количество значений " +
                         f"(ожидалось {expected}, получено {actual}).")


class InvalidTypeDeclarationError(DatabaseError, ValueError):
    def __init__(self, col_type: str, col_name: str):
        self.col_type = col_type
        self.col_name = col_name
        super().__init__(f"Ошибка: неверный тип '{col_type}' в '{col_name}'.")


class ParserError(Exception):
    """Ошибка разбора пользовательской команды."""
    def __init__(self, message: str):
        super().__init__(f"Некорректный ввод: {message}")
