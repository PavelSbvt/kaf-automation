import json
from dataclasses import asdict
from typing import List

from utils.output_rich import Rich


def save_itp_data(teachers_data: List):
    """
    Функция для записи данных о преподавателях, напарсенных из их индивидуального преподавательского плана
    :param teachers_data: массив с объектами датаклассов с информацией по каждому преподавателю отдельно
    :return: None
    """
    Rich.debug_log(f"Сохранение данных парсинга ИПП в json")
    with open("received_data/itp_data_teacher.json", "w", encoding = "utf-8") as file:
        json.dump([asdict(itp_data) for itp_data in teachers_data], file, ensure_ascii = False, indent = 2)
    Rich.success_log("Данные сохранены: received_data/itp_data_teacher.json")
