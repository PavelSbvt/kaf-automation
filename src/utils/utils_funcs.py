from pathlib import Path

from openpyxl import load_workbook, Workbook

from utils.output_rich import Rich


ROOT_DIRECTORY: Path = Path(__file__).resolve().parent.parent.parent
"""Путь к рабочей директории - корневой папке проекта"""
RESOURCES_DIRECTORY: Path = ROOT_DIRECTORY / "resources"
"""Путь от корневой папки проекта к папке ресурсов - 'resources'"""


def get_path_resources_file(file_path: str) -> str | None:
    """
    Функция для удобного получения безопасного пути к файлу, лежащему в папке resources
    :param file_path: путь к файлу (относительный)
    :return: str - рабочий путь, полученный с помощью pathlib
    """
    # Rich.debug_log(f"Проверка существования пути: {file_path}")
    pathlib_path = (RESOURCES_DIRECTORY / file_path).resolve()
    if pathlib_path.exists():
        # Rich.simple_log("Путь существует")
        return str(pathlib_path)
    else:
        Rich.warning_log(f"Указан несуществующий путь {file_path}")
        return None

def rounding(number: float | int) -> float:
    """
    Метод для округления числа до десятых

    :param number: принимает число

    :return: возвращает округлённое до десятых вещественное число
    """
    return round(float(number), 1)


def load_table(table_path: str) -> Workbook | None:
    """
    Функция для безопасной загрузки таблицы с предупреждением, если она не загрузится.
    Открывает таблицу в режиме только чтения информации

    :param table_path: путь к таблице

    :return: Workbook - книга для работы с openpyxl
    """
    try:
        Rich.print_spacer()
        Rich.debug_log("Попытка загрузки таблицы")
        ipt_workbook = load_workbook(table_path, data_only = True)
        Rich.simple_log(f"Загружена таблица: {table_path}")
        Rich.print_spacer()
        return ipt_workbook
    except Exception as e:
        Rich.warning_log(f"Не удалось загрузить таблицу. Ошибка {e}")
        Rich.print_spacer()
        return None
