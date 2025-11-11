from .exceptions import ParserError


def _parse_single_assignment(tokens: list[str]) -> dict:
    """
    Разбирает простое выражение присваивания вида <столбец> = <значение>.

    Args:
        tokens (list[str]): Список токенов, представляющих выражение.

    Returns:
        dict: Словарь с одним элементом {<столбец>: <значение>}.
    """
    
    if len(tokens) != 3 or tokens[1] != "=":
        raise ParserError( ' '.join(tokens))

    key, _, value = tokens

    if value.isdigit():
        value = int(value)
    elif value.lower() in ("true", "false"):
        value = value.lower() == "true"
    else:
        value = value.strip()

    return {key: value}


def parse_condition(condition: list[str]) -> dict:
    """
    Разбирает условие WHERE из списка токенов.

    Args:
        condition (list[str]): Токены, начиная с ключевого слова 'where'.

    Returns:
        dict: Словарь условия
    """

    if condition[0].lower() != "where":
        raise ParserError("ожидалось ключевое слово 'where'")

    return _parse_single_assignment(condition[1:])


def parse_update_parts(args: list[str]) -> tuple[dict, dict]:
    """
    Разбирает аргументы команды UPDATE на части SET и WHERE.

    Args:
        args (list[str]): Список токенов, начиная с 'set'.

    Returns:
        tuple[dict, dict]: Кортеж из двух словарей:
                           - set_clause: изменения (например, {"age": 30})
                           - where_clause: фильтр (например, {"id": 1}),
                           может быть пустым, если WHERE отсутствует.
    """
    
    if args[0].lower() != "set":
        raise ParserError("ожидалось ключевое слово 'set'")

    if "where" in args:
        where_index = args.index("where")
        set_part = args[1:where_index]
        where_part = args[where_index + 1:]
    else:
        set_part = args[1:]
        where_part = []

    set_clause = _parse_single_assignment(set_part)
    where_clause = _parse_single_assignment(where_part) if where_part else {}

    return set_clause, where_clause
