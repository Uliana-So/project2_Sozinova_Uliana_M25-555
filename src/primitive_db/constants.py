VALID_TYPES = {"int", "str", "bool"}
META_FILE = "db_meta.json"
INPUT_PROMT = "Введите команду: "

COMMANDS = {
    "create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ... ": "создать таблицу",
    "list_tables": "показать список всех таблиц",
    "drop_table <имя_таблицы>": "удалить таблицу",
    "exit": "выход из программы",
    "help": "справочная информация",
}
