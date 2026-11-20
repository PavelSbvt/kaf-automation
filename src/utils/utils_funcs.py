from pathlib import Path

from utils.output_rich import Rich


ROOT_DIRECTORY = Path(__file__).resolve().parent.parent.parent
RESOURCES_DIRECTORY = ROOT_DIRECTORY / "resources"

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
