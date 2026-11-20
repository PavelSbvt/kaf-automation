from openpyxl import load_workbook, Workbook

# from core.models import TeacherGeneralInfo
from utils.output_rich import Rich
from utils.utils_funcs import get_path_resources_file


def load_table(table_path: str) -> Workbook | None:
    """
    Функция для безопасной загрузки таблицы с исключением
    :param table_path: путь к таблице
    :return: Workbook
    """
    try:
        Rich.debug_log("Попытка загрузки таблицы")
        ipt_workbook = load_workbook(table_path)
        Rich.simple_log(f"Загружена таблица: {table_path}")
        return ipt_workbook
    except Exception as e:
        Rich.warning_log("Не удалось загрузить таблицу")
        return None

def parse_general_info_sheet(file_path: str):
    """
    Парсинг данных с листа "Общие сведения" из таблицы индивидуальный план преподавателя
    :return:
    """
    individual_plan = load_table(get_path_resources_file(file_path))
    # Открываю лист с общими сведениями
    individual_plan = individual_plan["Общие сведения"]
    # Вывод шапки листа
    Rich.debug_log(individual_plan['A1'].value)

    # Сбор данных
    # ========================================
    teacher_name = individual_plan['D3'].value
    Rich.debug_log(f"ФИО: {teacher_name}")

    teacher_post = individual_plan['D4'].value
    Rich.debug_log(f"Должность: {teacher_post}")

    teacher_amount_of_bet = float(individual_plan['D5'].value)
    Rich.debug_log(f"Размер ставки: {teacher_amount_of_bet}")

    teacher_terms_of_attraction = individual_plan['D6'].value
    Rich.debug_log(f"Условия привлечения: {teacher_terms_of_attraction}")

    teacher_academic_degree = individual_plan['D7'].value
    if teacher_academic_degree is None or teacher_academic_degree == "-":
        Rich.debug_log("Учёная степень: нет")
    else:
        Rich.debug_log(f"Учёная степень: {teacher_academic_degree}")

    teacher_academic_title = individual_plan['D8'].value
    if teacher_academic_title is None or teacher_academic_title == "-":
        Rich.debug_log("Учёное звание: нет")
    else:
        Rich.debug_log(f"Учёное звание: {teacher_academic_degree}")

    Rich.debug_log("--Сведения о контракте--")

    teacher_data_and_number = individual_plan['D10'].value
    Rich.debug_log(f"Дата, номер: {teacher_data_and_number}")

    teacher_validity_period = individual_plan['D11'].value
    Rich.debug_log(f"Срок действия: {teacher_validity_period}")

    Rich.debug_log("------------------------")

    teacher_basic_education = individual_plan['D12'].value
    Rich.debug_log(f"Базовое образование: {teacher_basic_education}")

    teacher_name_educational_program = individual_plan['D15'].value
    Rich.debug_log(f"Наименование образовательной программы: "
                   f"{teacher_name_educational_program}")

    teacher_qualification = individual_plan['D18'].value
    Rich.debug_log(f"Квалификация: {teacher_qualification}")

    teacher_list_subjects_taught = []

    # subjects_taught = individual_plan['A22'].value
    for iter in range(22, individual_plan.max_row):
        iter_subjects_taught = individual_plan[f'A{iter}'].value
        if iter_subjects_taught is None:
            break
        else:
            teacher_list_subjects_taught.append(iter_subjects_taught)

    Rich.debug_log(f"Перечень преподаваемых дисциплин: {teacher_list_subjects_taught}")

    # parsed_data = TeacherGeneralInfo(
    #     # ФИО
    #     name =
    #     # Должность
    #     post
    #     # Размер ставки
    #     amount_of_bet: float
    #     # Условия привлечения
    #     terms_of_attraction: str
    #     # Учёная степень
    #     academic_degree: str
    #     # Учёное звание
    #     academic_title: str
    #     # Сведения о контракте
    #     information_about_contract: str
    #     # Дата, номер
    #     date_and_number: str
    #     # Срок действия
    #     validity_period: str
    #     # Базовое образование
    #     basic_education: str
    #     # Наименование образовательной программы
    #     name_educational_program: str
    #     # Квалификация
    #     qualification: str
    #     # Перечень преподаваемых дисциплин
    #     list_subjects_taught: List
    # )
