def red_italics_text(text: str) -> str:
    """
    Возвращает строку, оформленную красным цветом курсивом с помощью ANSI-кодов.

    Args:
        text (str): Исходная строка.
    """

    return "\033[3m\033[31m{}\033[0m".format(text)


def bold_text(text: str) -> str:
    """
    Возвращает строку, оформленную полужирным стилем с помощью ANSI-кодов.

    Args:
        text (str): Исходная строка.
    """

    return "\033[1m{}\033[0m".format(text)


def italics_text(text: str) -> str:
    """
    Возвращает строку, оформленную курсивом с помощью ANSI-кодов.

    Args:
        text (str): Исходная строка.
    """

    return "\033[3m{}\033[0m".format(text)


def underlined_text(text: str) -> str:
    """
    Возвращает строку, оформленную с подчёркиванием с помощью ANSI-кодов.

    Args:
        text (str): Исходная строка.
    """

    return "\033[4m{}\033[0m".format(text)
