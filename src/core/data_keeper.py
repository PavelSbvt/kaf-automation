import json
from dataclasses import asdict
from typing import List

from core.models import (
    TeacherGeneralInfo,
    DataNamesOfWorksFromSummaryInfo,
    TeacherSummaryInfo,
    TeacherAcademicWorkPerSemester
)
from utils.output_rich import Rich


def save_itp_general_data(teachers_data: List[TeacherGeneralInfo]):
    """
    Функция для записи общих сведений преподавателей, напарсенных из их
    индивидуального преподавательского плана, в json
    :param teachers_data: массив с объектами датаклассов с информацией по каждому
     преподавателю отдельно
    :return: None
    """
    Rich.debug_log(f"Сохранение данных парсинга общих сведений из ИПП в json")
    with open("received_data/itp-teachers-general-data.json", "w", encoding = "utf-8") as file:
        json.dump([asdict(itp_general_data) for itp_general_data in teachers_data], file,
                  ensure_ascii = False, indent = 2)
    Rich.success_log("Данные сохранены: received_data/itp-teachers-general-data.json")
    Rich.print_spacer()


def save_itp_summary_data(teachers_data: List[TeacherSummaryInfo]):
    """
    Функция для записи сводных данных преподавателей, напарсенных из их
     индивидуального преподавательского плана, в json
    :param teachers_data: массив с объектами датаклассов с информацией по каждому
     преподавателю отдельно
    :return: None
    """
    Rich.debug_log(f"Сохранение данных парсинга сводных данных из ИПП в json")
    with open("received_data/itp-teachers-summary-data.json", "w", encoding = "utf-8") as file:
        json.dump([asdict(itp_summary_data) for itp_summary_data in teachers_data], file,
                  ensure_ascii = False, indent = 2)
    Rich.success_log("Данные сохранены: received_data/itp-teachers-summary-data.json")
    Rich.print_spacer()


def save_itp_educational_work_data(teachers_educational_work_data: List[TeacherAcademicWorkPerSemester]) -> None:
    """
    Функция для теста сохранения данных по учебной работе преподавателя за семестр
    :param teachers_educational_work_data: массив с массивами с датаклассами по учебной работе преподавателя из таблицы ИПП - пока тест
    :return: None
    """
    Rich.debug_log(f"Сохранение данных парсинга учебной работы преподавателя из ИПП в json")
    with open("received_data/itp-teachers-educational-work-data.json", "w", encoding="utf-8") as file:
        json.dump([asdict(itp_summary_data) for itp_summary_data in teachers_educational_work_data], file,
                  ensure_ascii=False, indent=2)
    Rich.success_log("Данные сохранены: received_data/itp-teachers-summary-data.json")
    Rich.print_spacer()
