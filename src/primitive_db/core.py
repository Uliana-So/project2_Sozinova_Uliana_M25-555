from .color_text import italics_text, red_italics_text
from .constants import META_FILE, VALID_TYPES
from .utils import save_metadata


class Database:
    """
    Класс содержит операции над переданными метаданными.
    """

    def create_table(self, metadata: dict, table_name: str, columns: list[tuple]) -> None: # noqa: E501
        """
        Создаёт новую таблицу в базе данных и обновляет метаданные.

        Args:
            metadata (dict): словарь-метаданные
            table_name (str): имя таблицы
            columns (list[tuple]): список столбцов и их типов

        Returns:
            dict: обновлённые метаданные
        """

        if table_name in metadata:
            print(red_italics_text(f"Ошибка: таблица '{table_name}' уже существует.\n"))
            return

        for name, col_type in columns:
            if col_type not in VALID_TYPES:
                print(red_italics_text(f"Ошибка: неверный тип '{col_type}' в '{name}'\n")) # noqa: E501
                return

        metadata[table_name] = [("ID", "int")] + columns
        save_metadata(META_FILE, metadata)
        print(italics_text(f"Таблица '{table_name}' успешно создана со столбцами: " +
              ", ".join(f"{name}:{dtype}" for name, dtype in columns) + "\n"))

    def drop_table(self, metadata: dict, table_name: str) -> None:
        """
        Удаляет таблицу из базы данных и обновляет метаданные.

        Args:
            metadata (dict): Текущие метаданные базы данных.
            table_name (str): Название таблицы.

        Returns:
            dict
        """

        if table_name not in metadata:
            print(red_italics_text(f"Ошибка: таблицы '{table_name}' не существует.\n"))
            return 

        del metadata[table_name]
        save_metadata(META_FILE, metadata)
        print(italics_text(f"Таблица '{table_name}' успешно удалена.\n"))

    def list_tables(self, metadata: dict) -> None:
        """
        Выводит список всех таблиц.

        Args:
            metadata (dict): Текущие метаданные базы данных.
        """

        print(*[f"- {t}" for t in metadata.keys()], sep="\n")
        print()
