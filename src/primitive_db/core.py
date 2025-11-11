from .color_text import italics_text
from .constants import META_FILE
from .parser import parse_condition, parse_update_parts
from .utils import load_table_data, print_prettytable, save_metadata, save_table_data


class Database:
    """
    Класс для управления файловой базой данных.

    Метаданные (описание таблиц и схемы столбцов) и данные таблиц хранятся
    в JSON-файлах.

    Возможности:
        • Создание и удаление таблиц.
        • Управление метаданными таблиц.
        • Поддержка CRUD:
            - insert: добавление новой строки
            - select: получение данных с фильтрацией
            - update: изменение существующих записей
            - delete: удаление записей

    Атрибуты класса:
        VALID_TYPES (set[str]):
            Набор поддерживаемых типов данных столбцов:
            {"int", "str", "bool"}.
    """

    VALID_TYPES = {"int", "str", "bool"}

    def create_table(self, metadata: dict, table_name: str, columns: list[tuple]) -> None: # noqa: E501
        """Создаёт новую таблицу в базе данных и обновляет метаданные."""
        if table_name in metadata:
            raise ValueError(f"Ошибка: таблица '{table_name}' уже существует.")

        for name, col_type in columns:
            if col_type not in self.VALID_TYPES:
                raise ValueError(f"Ошибка: неверный тип '{col_type}' в '{name}'\n") # noqa: E501

        metadata[table_name] = [("ID", "int")] + columns
        save_metadata(META_FILE, metadata)
        columns_str = ", ".join(f"{name}:{type}" for name, type in columns)
        print(italics_text(f"Таблица '{table_name}' успешно создана со столбцами: {columns_str}"))  # noqa: E501

    def drop_table(self, metadata: dict, table_name: str) -> None:
        """Удаляет таблицу из базы данных и обновляет метаданные."""
        self._check_tablename(metadata, table_name)
        
        del metadata[table_name]
        save_metadata(META_FILE, metadata)
        print(italics_text(f"Таблица '{table_name}' успешно удалена."))

    def list_tables(self, metadata: dict) -> None:
        """Выводит список всех таблиц."""
        print(*[f"- {t}" for t in metadata.keys()], sep="\n")

    def insert(self, metadata: str, table_name: str, values: list[str]) -> None:
        """Вставляет новую запись согласно схеме таблицы"""
        self._check_tablename(metadata, table_name)

        schema = metadata[table_name]
        expected = schema[1:]  # без ID
        if len(values) != len(expected):
            raise ValueError("Ошибка: неверное количество значений.")

        data = load_table_data(table_name)
        new_id = (max(row["ID"] for row in data) + 1) if data else 1
        new_row = {"ID": new_id}

        for (col_name, col_type), val in zip(expected, values):
            val = val.strip(" (),\"'")
            if col_type not in self.VALID_TYPES:
                raise ValueError(f"Ошибка: неверный тип для '{col_name}'.")

            if col_type == "int":
                new_row[col_name] = int(val)
            elif col_type == "bool":
                new_row[col_name] = val.lower() == "true"
            else:
                new_row[col_name] = str(val)

        data.append(new_row)
        save_table_data(table_name, data)
        print(italics_text(f"Запись с ID={new_id} в таблицу '{table_name}' успешно обновлена.")) # noqa: E501

    def select(self, metadata: dict, table_name: str, condition: list[str] | None) -> None: # noqa: E501
        """Получает записи по условию."""
        self._check_tablename(metadata, table_name)

        data = load_table_data(table_name)
        if not data:
            return

        columns = data[0].keys()
        if condition:
            filters = parse_condition(condition)
            data = [row for row in data if all(row.get(k) == v for k, v in filters.items())] # noqa: E501

        print_prettytable(columns, data)

    def update(self, metadata: dict, table_name: str, clause: list[str]) -> None:
        """Обновляет данные по условию"""
        self._check_tablename(metadata, table_name)
        
        set_clause, where_clause = parse_update_parts(clause)
        data = load_table_data(table_name)
        count = 0

        for row in data:
            if not where_clause or all(row.get(k) == v for k, v in where_clause.items()): # noqa: E501
                for s_key, s_val in set_clause.items():
                    row[s_key] = s_val
                count += 1

        save_table_data(table_name, data)
        print(italics_text(f"Обновлено записей: {count}"))

    def delete(self, metadata: dict, table_name: str, condition: list[str]) -> None:
        """Удаляет данные по условию"""
        self._check_tablename(metadata, table_name)

        data = load_table_data(table_name)
        filters = parse_condition(condition)
        key, value = next(iter(filters.items()))
        new_data = [r for r in data if r.get(key) != value]

        save_table_data(table_name, new_data)
        print(italics_text(f"Удалено записей: {len(data) - len(new_data)}"))

    def info(self, metadata: dict, table_name: str):
        """Выводит информацию о таблице."""
        self._check_tablename(metadata, table_name)

        data = load_table_data(table_name)
        columns = metadata[table_name]
        columns_str = ", ".join(f"{name}:{type}" for name, type in columns)
        print(italics_text(f"Таблица: {table_name}"))
        print(italics_text(f"Столбцы: {columns_str}"))
        print(italics_text(f"Количество записей: {len(data)}"))

    @staticmethod
    def _check_tablename(metadata: dict, table_name: str) -> None:
        if table_name not in metadata:
            raise ValueError(f"Ошибка: таблицы '{table_name}' не существует.")
