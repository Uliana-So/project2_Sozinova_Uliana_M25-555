import json
import os
from typing import Any, Callable

from prettytable import PrettyTable

from .color_text import bold_text, underlined_text
from .constants import DATA_DIR


def load_metadata(filepath: str) -> dict :
    """
    Загружает метаданные из JSON-файла.

    Args:
        filepath (str): Путь к JSON-файлу.

    Returns:
        dict: Метаданные или пустой словарь {} при отсутствии файла.
    """

    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


def save_metadata(filepath: str, data: dict) -> None:
    """
    Сохраняет метаданные в JSON-файл.

    Args:
        filepath (str): Путь для сохранения JSON-файла.
        data (dict): Данные для сохранения.
    """
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_table_data(table_name: str) -> list:
    """
    Загружает данные таблицы из JSON-файла.

    Args:
        table_name (str): Название таблицы.

    Returns:
        list: Список записей таблицы.
    """

    filepath = os.path.join(DATA_DIR, f"{table_name}.json")

    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


def save_table_data(table_name: str, data: list) -> None:
    """
    Сохраняет данные таблицы в JSON-файл.

    Args:
        table_name (str): Название таблицы.
        data (list): Список записей таблицы.
    """

    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def print_prettytable(columns: list, data: dict):
    """
    Выводит таблицу с использованием библиотеки PrettyTable.

    Args:
        columns (list): Названия колонок.
        data (dict): Данные таблицы.
    """

    table = PrettyTable()
    table.field_names = columns
    if data:
        for row in data:
            table.add_row(row.values())
    print(table)


def print_help(commands: dict) -> None:
    """
    Выводит список доступных функций и их описания.

    Args:
        commands (dict): Словарь функций и их описаний
    """

    print(bold_text("\n***   Процесс работы с таблицей   ***"))
    print(underlined_text("Функции:"))
    for i, v in commands.items():
        print(f"{i:<30} — {v}")


def create_cacher():
    """
    Создает кэш с замыканием для каждой таблицы.

    Returns:
        cache_result: Функция, которая принимает название таблицы,
        ключ и функцию value_func.
    """

    _cache = {}  # это словарь для замыкания

    def cache_result(table_name: str, key: str, value_func: Callable[[], Any]) -> Any:
        """
        Возвращает результат по ключу из кэша или вызывает value_func, если его нет.

        Args:
            table_name (str): Название таблицы
            key (str): Ключ для кэширования
            value_func (Callable): Функция, возвращающая значение, если его нет в кэше

        Returns:
            Any: Значение, возвращаемое value_func
        """

        if table_name not in _cache:
            _cache[table_name] = {}

        table_cache = _cache[table_name]

        if key in table_cache:
            return table_cache[key]

        result = value_func()
        table_cache[key] = result
        return result

    def clear(table_name: str | None) -> None:
        """
        Очищает кэш для конкретной таблицы или весь кэш.

        Args:
            table_name (str): Название таблицы
        """

        if table_name:
            _cache.pop(table_name, None)
        else:
            _cache.clear()

    cache_result.clear = clear

    return cache_result
