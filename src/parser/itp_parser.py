import re
from typing import List

from openpyxl import load_workbook, Workbook

from core.models import (
    TeacherGeneralInfo,
    DataNamesOfWorksFromSummaryInfo,
    TeacherSummaryInfo)
from utils.output_rich import Rich
from utils.utils_funcs import get_path_resources_file


# Список с объектами датаклассов с основной информацией преподавателя из ИПП
ITP_TEACHERS_GENERAL_DATA: List[TeacherGeneralInfo] = []
# Список с объектами датаклассов со сводными данными по видам работ преподавателя
ITP_TEACHERS_SUMMARY_DATA: List[TeacherSummaryInfo] = []


def load_table(table_path: str) -> Workbook | None:
    """
    Функция для безопасной загрузки таблицы с исключением
    :param table_path: путь к таблице
    :return: Workbook
    """
    try:
        Rich.print_spacer()
        Rich.debug_log("Попытка загрузки таблицы")
        ipt_workbook = load_workbook(table_path, data_only = True)
        Rich.simple_log(f"Загружена таблица: {table_path}")
        Rich.print_spacer()
        return ipt_workbook
    except Exception as e:
        Rich.warning_log("Не удалось загрузить таблицу")
        Rich.print_spacer()
        return None


def parse_general_info_sheet(file_path: str) -> None:
    """
    Парсинг данных с листа "Общие сведения" из таблицы индивидуального плана преподавателя
    :return: None
    """
    individual_plan = load_table(get_path_resources_file(file_path))
    # Открываю лист с общими сведениями
    general_info = individual_plan["Общие сведения"]
    Rich.print_spacer()
    # Вывод шапки листа
    Rich.simple_log(general_info['A1'].value)

    # Сбор данных
    # ========================================
    teacher_name = general_info['D3'].value
    Rich.debug_log(f"ФИО: {teacher_name}")

    teacher_post = general_info['D4'].value
    Rich.debug_log(f"Должность: {teacher_post}")

    teacher_amount_of_bet = float(general_info['D5'].value)
    Rich.debug_log(f"Размер ставки: {teacher_amount_of_bet}")

    teacher_terms_of_attraction = general_info['D6'].value
    Rich.debug_log(f"Условия привлечения: {teacher_terms_of_attraction}")

    teacher_academic_degree = general_info['D7'].value
    if teacher_academic_degree is None or teacher_academic_degree == "-":
        Rich.debug_log("Учёная степень: нет")
        teacher_academic_degree = None
    else:
        Rich.debug_log(f"Учёная степень: {teacher_academic_degree}")

    teacher_academic_title = general_info['D8'].value
    if teacher_academic_title is None or teacher_academic_title == "-":
        Rich.debug_log("Учёное звание: нет")
        teacher_academic_title = None
    else:
        Rich.debug_log(f"Учёное звание: {teacher_academic_degree}")

    Rich.print_spacer_points()
    Rich.debug_log("Сведения о контракте")

    teacher_data_and_number = general_info['D10'].value
    Rich.debug_log(f"Дата, номер: {teacher_data_and_number}")

    teacher_validity_period = general_info['D11'].value
    Rich.debug_log(f"Срок действия: {teacher_validity_period}")

    Rich.print_spacer_points()

    teacher_basic_education = general_info['D12'].value
    Rich.debug_log(f"Базовое образование: {teacher_basic_education}")

    teacher_name_educational_program = general_info['D15'].value
    Rich.debug_log(f"Наименование образовательной программы: "
                   f"{teacher_name_educational_program}")

    teacher_qualification = general_info['D18'].value
    Rich.debug_log(f"Квалификация: {teacher_qualification}")

    teacher_list_subjects_taught = []

    for iter in range(22, general_info.max_row):
        iter_subjects_taught = general_info[f'A{iter}'].value
        if iter_subjects_taught is None:
            break
        else:
            iter_cleared_of_numbering = re.sub(r"^\s*\d+\s*\.\s*", "", iter_subjects_taught)
            if iter_cleared_of_numbering == "":
                break
            else:
                teacher_list_subjects_taught.append(iter_subjects_taught)

    Rich.debug_log(f"Перечень преподаваемых дисциплин:")
    for subject in teacher_list_subjects_taught:
        Rich.debug_log(f"   {subject}")

    parsed_data = TeacherGeneralInfo(
        # ФИО
        name = teacher_name,
        # Должность
        post = teacher_post,
        # Размер ставки
        amount_of_bet = teacher_amount_of_bet,
        # Условия привлечения
        terms_of_attraction = teacher_terms_of_attraction,
        # Учёная степень
        academic_degree = teacher_academic_degree,
        # Учёное звание
        academic_title = teacher_academic_title,
        # Сведения о контракте
        # Дата, номер
        date_and_number = teacher_data_and_number,
        # Срок действия
        validity_period = teacher_validity_period,
        # Базовое образование
        basic_education = teacher_basic_education,
        # Наименование образовательной программы
        name_educational_program = teacher_name_educational_program,
        # Квалификация
        qualification = teacher_qualification,
        # Перечень преподаваемых дисциплин
        list_subjects_taught = teacher_list_subjects_taught
    )

    ITP_TEACHERS_GENERAL_DATA.append(parsed_data)
    Rich.print_spacer()

    return None


def parse_summary_data(file_path: str) -> None:
    """
    Функция для паргинга листа "Сводные данные" из таблицы ИПП
    :return: None
    """
    individual_plan = load_table(get_path_resources_file(file_path))
    # Открываю лист со сводными данными
    summary_data = individual_plan["Сводные данные"]
    Rich.print_spacer()
    # Вывод шапки листа
    Rich.simple_log(summary_data['A1'].value)

    # парсинг ячеек с данными
    # За какой год указана информация
    teachers_year_is_amount_of_work_indicated = summary_data['B3'].value
    Rich.debug_log(f"{teachers_year_is_amount_of_work_indicated}")

    # список с информацией о работах преподавателя
    teacher_jobs_info: List[DataNamesOfWorksFromSummaryInfo] = []

    teachers_total_number_of_hours = -1

    for iter in range(5, summary_data.max_row):
        iter_cell_with_type_of_work =  summary_data[f'A{iter}'].value
        iter_cell_with_type_of_work = " ".join(iter_cell_with_type_of_work.split())
        cell_with_number_of_hours = summary_data[f'B{iter}'].value
        if not cell_with_number_of_hours is None:
            iter_cell_with_number_of_hours = round(float(summary_data[f'B{iter}'].value), 1)
        else:
            iter_cell_with_number_of_hours = 0.0
        if iter_cell_with_type_of_work is None:
            break
        else:
            if "в том числе:" in iter_cell_with_type_of_work:
                continue
            if "Всего:" in iter_cell_with_type_of_work:
                teachers_total_number_of_hours = round(float(iter_cell_with_number_of_hours), 1)
                break
            else:
                row_data = DataNamesOfWorksFromSummaryInfo(
                    activity_name = iter_cell_with_type_of_work,
                    amount_work_hours = iter_cell_with_number_of_hours
                )
                teacher_jobs_info.append(row_data)

    summary_data_from_table = TeacherSummaryInfo(
        year_is_amount_of_work_indicated = teachers_year_is_amount_of_work_indicated,
        list_data_of_names_of_works = teacher_jobs_info,
        total_hours = teachers_total_number_of_hours
    )

    Rich.debug_log(f"Наименование работ и видов деятельности:")
    for subject in teacher_jobs_info:
        Rich.debug_log(f"   {subject.activity_name}: {subject.amount_work_hours}")

    Rich.debug_log(f"Всего: {teachers_total_number_of_hours}")

    ITP_TEACHERS_SUMMARY_DATA.append(summary_data_from_table)
    Rich.print_spacer()
