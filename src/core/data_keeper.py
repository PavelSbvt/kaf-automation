import json
from dataclasses import asdict
from typing import List

from core.models import (
    TeacherGeneralInfo,
    DataNamesOfWorksFromSummaryInfo,
    TeacherSummaryInfo,
    TeacherAcademicWorkPerSemester,
    FullInfoOnEducationWorkOfTeacher,
    TeacherEducationalAndMethodicalWorkData,
    TeacherScientificAndResearchInfo,
    TeacherOrgAndPedagogicalInfo,
    TeachersProfessionalDevelopmentInfo)
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


def save_itp_educational_work_data(teachers_educational_work_data: List[FullInfoOnEducationWorkOfTeacher]) -> None:
    """
    Функция для теста сохранения данных по учебной работе преподавателя за семестр
    :param teachers_educational_work_data: массив с массивами с датаклассами по учебной работе преподавателя из таблицы ИПП
    :return: None
    """
    Rich.debug_log(f"Сохранение данных парсинга учебной работы преподавателя из ИПП в json")
    with open("received_data/itp-teachers-educational-work-data.json", "w", encoding="utf-8") as file:
        json.dump([asdict(itp_summary_data) for itp_summary_data in teachers_educational_work_data], file,
                  ensure_ascii=False, indent=2)
    Rich.success_log("Данные сохранены: received_data/itp-teachers-educational-work-data.json")
    Rich.print_spacer()


def save_itp_educational_and_methodical_work_data(teachers_data: List[TeacherEducationalAndMethodicalWorkData]) -> None:
    """
    Функция для теста сохранения данных по учебно-методической работе преподавателя
    :param teachers_data: массив с массивами с датаклассами по учебно-методической работе преподавателя из таблицы ИПП
    :return: None
    """
    Rich.debug_log(f"Сохранение данных парсинга учебно-методической работы преподавателя из ИПП в json")
    with open("received_data/itp-teachers-educational-and-methodical-work-data.json", "w", encoding="utf-8") as file:
        json.dump([asdict(itp_data) for itp_data in teachers_data], file,
                  ensure_ascii=False, indent=2)
    Rich.success_log("Данные сохранены: received_data/itp-teachers-educational-and-methodical-work-data.json")
    Rich.print_spacer()


def save_itp_scientific_and_research_data(teachers_data: List[TeacherScientificAndResearchInfo]) -> None:
    """
    Функция для теста сохранения данных по научно-исследовательской деятельности преподавателя
    :param teachers_data: массив с массивами с датаклассами по научно-исследовательской деятельности преподавателя из таблицы ИПП
    :return: None
    """
    Rich.debug_log(f"Сохранение данных парсинга научно-исследовательской деятельности преподавателя из ИПП в json")
    with open("received_data/itp-teachers-scientific-and-research-work-data.json", "w", encoding="utf-8") as file:
        json.dump([asdict(itp_data) for itp_data in teachers_data], file,
                  ensure_ascii=False, indent=2)
    Rich.success_log("Данные сохранены: received_data/itp-teachers-scientific-and-research-work-data.json")
    Rich.print_spacer()


def save_itp_organization_and_pedagogical_data(
        teachers_data: List[TeacherOrgAndPedagogicalInfo]) -> None:
    """
    Функция для теста сохранения данных по организационной и воспитательной
     деятельности преподавателя
    :param teachers_data: массив с массивами с датаклассами по организационной
     и воспитательной деятельности преподавателя из таблицы ИПП
    :return: None
    """
    Rich.debug_log(f"Сохранение данных парсинга организационной и воспитательной"
                   f" деятельности преподавателя из ИПП в json")
    with open("received_data/itp-teachers-organization-and-pedagogical-work-data.json",
              "w", encoding="utf-8") as file:
        json.dump([asdict(itp_data) for itp_data in teachers_data], file,
                  ensure_ascii=False, indent=2)
    Rich.success_log("Данные сохранены: "
                     "received_data/itp-teachers-organization-and-pedagogical-work-data.json")
    Rich.print_spacer()

def save_itp_professional_development_data(
        teachers_data: List[TeachersProfessionalDevelopmentInfo]) -> None:
    """
    Функция для теста сохранения данных о повышении квалификации
     преподавателя
    :param teachers_data: массив с массивами с датаклассами с данными о повышении
     квалификации преподавателя из таблицы ИПП
    :return: None
    """
    Rich.debug_log(f"Сохранение данных парсинга о повышении квалификации"
                   f" преподавателя из ИПП в json")
    with open("received_data/itp-teachers-professional_development-data.json",
              "w", encoding="utf-8") as file:
        json.dump([asdict(itp_data) for itp_data in teachers_data], file,
                  ensure_ascii=False, indent=2)
    Rich.success_log("Данные сохранены: "
                     "received_data/itp-teachers-professional_development-data.json")
    Rich.print_spacer()