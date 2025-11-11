import json
import os

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

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:

        return {}


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
        table_name (str): Имя таблицы.

    Returns:
        list: Список записей таблицы.
    """

    filepath = os.path.join(DATA_DIR, f"{table_name}.json")

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_table_data(table_name: str, data: list) -> None:
    """
    Сохраняет данные таблицы в JSON-файл.

    Args:
        table_name (str): Имя таблицы.
        data (list): Список записей таблицы.
    """

    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def print_prettytable(columns: dict, data: dict):
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
        commands (dict): словарь функций и их описаний
    """

    print(bold_text("\n***   Процесс работы с таблицей   ***"))
    print(underlined_text("Функции:"))
    for i, v in commands.items():
        print(f"{i:<30} — {v}")
