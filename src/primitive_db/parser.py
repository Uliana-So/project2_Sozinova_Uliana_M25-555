def _parse_single_assignment(tokens: list[str]) -> dict:
    if len(tokens) != 3 or tokens[1] != "=":
        raise ValueError(f"Неверный формат выражения: {' '.join(tokens)}")

    key, _, value = tokens

    if value.isdigit():
        value = int(value)
    elif value.lower() in ("true", "false"):
        value = value.lower() == "true"
    else:
        value = value.strip()

    return {key: value}


def parse_condition(condition: list[str]) -> dict:
    if condition[0].lower() != "where":
        raise ValueError("Некорректная команда: ожидалось ключевое слово 'where'.")

    return _parse_single_assignment(condition[1:])


def parse_update_parts(args: list[str]) -> tuple[dict, dict]:
    if args[0].lower() != "set":
        raise ValueError("Некорректная команда: ожидалось ключевое слово 'set'.")

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