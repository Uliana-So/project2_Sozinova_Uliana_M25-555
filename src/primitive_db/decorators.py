import time

import prompt

from .color_text import faded_text, italics_text, red_italics_text
from .exceptions import (
    ColumnCountError,
    InvalidTypeDeclarationError,
    ParserError,
    TableExistsError,
    TableNotFoundError,
)


def handle_db_errors(func):
    """
    Декоратор для обработки ошибок.
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ParserError as e:
            print(red_italics_text(e.args[0]))
        except TableNotFoundError as e:
            print(red_italics_text(e.args[0]))
        except TableExistsError as e:
            print(red_italics_text(e.args[0]))
        except ColumnCountError as e:
            print(red_italics_text(e.args[0]))
        except InvalidTypeDeclarationError as e:
            print(red_italics_text(e.args[0]))
        except FileNotFoundError:
            print(red_italics_text("Ошибка: Файл данных не найден. " +
                                   "Возможно, база данных не инициализирована."))
        except Exception as e:
            print(red_italics_text(f"Произошла непредвиденная ошибка: {e}"))
    
    return wrapper


def confirm_action(action_name: str):
    """
    Декоратор с аргументом — запрашивает подтверждение перед 
    выполнением опасного действия.
    
    Args:
        action_name (str): Название операции для отображения в сообщении пользователю.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            response = prompt.string("Вы уверены, что хотите выполнить " +
                                     f"'{action_name}'? [y/n]: ").strip().lower()
            if response != "y":
                print(italics_text("Операция отменена пользователем."))
                return
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


def log_time(func):
    """
    Декоратор замеряет время выполнения функции.
    """

    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        execution_time = end_time - start_time
        print(faded_text(f"Функция <{func.__name__}> выполнилась за " +
                         f"{execution_time:.4f} секунд"))
        return result
    
    return wrapper
