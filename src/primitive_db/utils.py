import json


def load_metadata(filepath:str) -> dict :
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


def save_metadata(filepath, data) -> None:
    """
    Сохраняет метаданные в JSON-файл.

    Args:
        filepath (str): Путь для сохранения JSON-файла.
        data (dict): Данные для сохранения.
    """
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
