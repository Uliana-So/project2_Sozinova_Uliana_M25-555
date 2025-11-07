import shlex

import prompt

from .color_text import bold_text, red_italics_text, underlined_text
from .constants import COMMANDS, INPUT_PROMT, META_FILE
from .core import Database
from .utils import load_metadata


def print_help(commands: dict) -> None:
    """
    Выводит список доступных функций и их описания.

    Args:
        commands (dict): словарь функций и их описаний
    """

    print(bold_text("\n***   Процесс работы с таблицей   ***"))
    print(underlined_text("Функции:"))
    for i, v in commands.items():
        print(f"{i:<25} — {v}")
    print()



def process_command(db: Database, metadata: dict, cmd: str):
    """
    Обрабатывает пользовательскую команду базы данных и вызывает соответствующий метод.

    Args:
        db (Database): Экземпляр класса Database для взаимодействия с таблицами.
        metadata (dict): Текущие метаданные базы данных.
        cmd (str): Введенная пользователем строка с командой и аргументами.
    """

    split_cmd = shlex.split(cmd)
    match split_cmd[0]:
        case "create_table":
            columns = [col.split(":") for col in split_cmd[2:]]
            db.create_table(metadata, split_cmd[1], columns)
        case "list_tables":
            db.list_tables(metadata)
        case "drop_table":
            db.drop_table(metadata, split_cmd[1])
        case "help":
            print_help(COMMANDS)
        case "exit":
            exit()
        case _:
            print(red_italics_text(f"Функции <{cmd}> нет. Попробуйте снова.\n"))


def run():
    """
    Главный цикл приложения для управления базой данных.
    """
    
    print_help(COMMANDS)

    db = Database()
    while True:
        metadata = load_metadata(META_FILE)
        user_input = prompt.string(INPUT_PROMT).strip()
        process_command(db, metadata, user_input)
