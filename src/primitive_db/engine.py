import shlex

import prompt

from .color_text import red_italics_text
from .constants import COMMANDS, INPUT_PROMT, META_FILE
from .core import Database
from .utils import load_metadata, print_help


def process_command(db: Database, metadata: dict, cmd: str):
    """
    Обрабатывает пользовательскую команду базы данных и вызывает соответствующий метод.

    Args:
        db (Database): Экземпляр класса Database для взаимодействия с таблицами.
        metadata (dict): Текущие метаданные базы данных.
        cmd (str): Введенная пользователем строка с командой и аргументами.
    """

    split_cmd = shlex.split(cmd.strip())

    match split_cmd[0].lower():
        case "create_table":
            if len(split_cmd) < 3:
                raise ValueError(f"Некорректная функция: {cmd}. Попробуйте снова.")
            columns = [col.split(":") for col in split_cmd[2:]]
            db.create_table(metadata, split_cmd[1], columns)
        
        case "list_tables":
            db.list_tables(metadata)
        
        case "drop_table":
            if len(split_cmd) < 2:
                raise ValueError(f"Некорректная функция: {cmd}. Попробуйте снова.")
            db.drop_table(metadata, split_cmd[1])
        
        case "insert":
            if len(split_cmd) < 5:
                raise ValueError(f"Некорректная функция: {cmd}. Попробуйте снова.")
            db.insert(metadata, split_cmd[2], split_cmd[4:])

        case "select":
            if len(split_cmd) < 3:
                raise ValueError(f"Некорректная функция: {cmd}. Попробуйте снова.")
            db.select(metadata, split_cmd[2], split_cmd[3:])

        case "update":
            if len(split_cmd) < 6:
                raise ValueError(f"Некорректная функция: {cmd}. Попробуйте снова.")
            db.update(metadata, split_cmd[1], split_cmd[2:])

        case "delete":
            if len(split_cmd) < 4:
                raise ValueError(f"Некорректная функция: {cmd}. Попробуйте снова.")
            db.delete(metadata, split_cmd[2], split_cmd[3:])

        case "info":
            if len(split_cmd) < 2:
                raise ValueError(f"Некорректная функция: {cmd}. Попробуйте снова.")
            db.info(metadata, split_cmd[1])

        case "help":
            print_help(COMMANDS)

        case "exit":
            exit()

        case _:
            raise ValueError(f"Функции <{split_cmd[0]}> нет. Попробуйте снова.")


def run():
    """
    Главный цикл приложения для управления базой данных.
    """
    
    print_help(COMMANDS)

    db = Database()
    while True:
        try:
            metadata = load_metadata(META_FILE)
            user_input = prompt.string(INPUT_PROMT)
            process_command(db, metadata, user_input)
        except (ValueError) as error:
            print(red_italics_text(error))
        except (KeyboardInterrupt, EOFError):
            break
