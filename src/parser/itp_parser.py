import re
from typing import List

from openpyxl import load_workbook, Workbook

from core.models import (
    TeacherGeneralInfo,
    DataNamesOfWorksFromSummaryInfo,
    TeacherSummaryInfo,
    InformationOnDisciplineOfAcademicWork,
    TeachersSummaryInfoOnHoursOfWorkPerSemester,
    TeacherAcademicWorkPerSemester)
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
        Rich.warning_log(f"Не удалось загрузить таблицу. Ошибка {e}")
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


def parse_summary_data_sheet(file_path: str) -> None:
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


list_with_semesters_data: List[TeacherAcademicWorkPerSemester] = []

def parse_educational_work_sheet(file_path: str) -> None:
    """
    Функция для парсинга листа 1.1 "Учебная работа" из талицы ИПП для получения
    информации о дисциплинах, типах занятий, количестве часов, группах и
    другой информации по учебной работе преподавателя.
    :param file_path: путь к файлу таблицы
    :return: None
    """
    individual_plan = load_table(get_path_resources_file(file_path))
    # Открываю лист с учебной работой - лист 1.1.
    educational_work_data = individual_plan["1.1. "]
    Rich.print_spacer()
    # Вывод шапки листа
    Rich.simple_log(" ".join((educational_work_data['A1'].value).split()))

    current_semester = ""
    subject_name = ""
    current_group = ""
    educational_semester = -1
    hours_of_lectures = -1.0
    hours_of_practice_lessons = -1.0
    hours_of_laboratory_work = -1.0
    hours_of_consultations = -1.0
    hours_of_exams = -1.0
    hours_of_credits = -1.0
    hours_of_terms_works = -1.0
    hours_of_practice = -1.0
    hours_WRC = -1.0
    hours_of_GEC = -1.0
    hours_of_additional_works = -1.0
    hours_of_total_according_to_plan = -1.0
    hours_of_total_actually = -1.0

    list_of_disciplines_in_semester: List[InformationOnDisciplineOfAcademicWork] = []

    for row in range(5, educational_work_data.max_row - 4):
        # парсинг данных

        # парсинг по дисциплинам

        # семестр
        if not educational_work_data[f"A{row}"].value is None:
            if ("семестр" in educational_work_data[f"A{row}"].value
                    and not ("Итого за семестр"
                             in educational_work_data[f"A{row}"].value)
                    and not ("Фактически выполнено за семестр"
                             in educational_work_data[f"A{row}"].value)):
                current_semester = educational_work_data[f"A{row}"].value
                Rich.simple_log(f"Семестр: {current_semester}")

        if (not educational_work_data[f'A{row}'].value is None
            and not "семестр" in educational_work_data[f'A{row}'].value):

            # Дальше парсинг данных по дисциплинам
            # название дисциплины
            subject_name = educational_work_data[f'A{row}'].value
            Rich.debug_log(f"Дисциплина: {subject_name}")

            # Группа
            if not educational_work_data[f'C{row}'].value is None:
                current_group = educational_work_data[f'C{row}'].value
                Rich.debug_log(f"Группа: {current_group}")

            # Номер семестра (семестра обучения группы)
            educational_semester = educational_work_data[f'D{row}'].value
            Rich.debug_log(f"Номер семестра: {educational_semester}")

            # Количество часов лекций
            hours_of_lectures = educational_work_data[f'E{row}'].value
            if hours_of_lectures is None:
                hours_of_lectures = 0
            Rich.debug_log(f"Часов лекций: {hours_of_lectures}")

            # Количество часов практики
            hours_of_practice_lessons = educational_work_data[f'F{row}'].value
            if  hours_of_practice_lessons is None:
                hours_of_practice_lessons = 0
            Rich.debug_log(f"Часов практики: {hours_of_practice_lessons}")

            # Количество часов лабораторных работ
            hours_of_laboratory_work = educational_work_data[f'G{row}'].value
            if hours_of_laboratory_work is None:
                hours_of_laboratory_work = 0
            Rich.debug_log(f"Часов лабораторных работ: {hours_of_laboratory_work}")

            # Количество часов консультаций
            hours_of_consultations = educational_work_data[f'H{row}'].value
            if hours_of_consultations is None:
                hours_of_consultations = 0
            Rich.debug_log(f"Часов консультаций: {hours_of_consultations}")

            # Часов экзаменов
            hours_of_exams = educational_work_data[f'I{row}'].value
            if hours_of_exams is None:
                hours_of_exams = 0
            Rich.debug_log(f"Часов экзаменов: {hours_of_exams}")

            # Часов зачётов
            hours_of_credits = educational_work_data[f'J{row}'].value
            if hours_of_credits is None:
                hours_of_credits = 0
            Rich.debug_log(f"Часов зачётов: {hours_of_credits}")

            # Часов курсовых работ, курсовых проектов
            hours_of_terms_works = educational_work_data[f'K{row}'].value
            if hours_of_terms_works is None:
                hours_of_terms_works = 0
            Rich.debug_log(f"Часов курсовых работ, курсовых проектов: {hours_of_terms_works}")

            # Часов практики
            hours_of_practice = educational_work_data[f'L{row}'].value
            if hours_of_practice is None:
                hours_of_practice = 0
            Rich.debug_log(f"Часов практики: {hours_of_practice}")

            # Часов ВКП
            hours_WRC = educational_work_data[f'M{row}'].value
            if hours_WRC is None:
                hours_WRC = 0
            Rich.debug_log(f"Часов ВКР: {hours_WRC}")

            # Часов ГЭК
            hours_of_GEC = educational_work_data[f'N{row}'].value
            if hours_of_GEC is None:
                hours_of_GEC = 0
            Rich.debug_log(f"Часов ГЭК: {hours_of_GEC}")

            # Часов дополнительных работ
            hours_of_additional_works = educational_work_data[f'O{row}'].value
            if hours_of_additional_works is None:
                hours_of_additional_works = 0
            Rich.debug_log(f"Часов дополнительных работ: {hours_of_additional_works}")

            # Всего часов по плану
            hours_of_total_according_to_plan = educational_work_data[f'P{row}'].value
            if hours_of_total_according_to_plan is None:
                hours_of_total_according_to_plan = 0
            Rich.debug_log(f"Всего часов по плану: {hours_of_total_according_to_plan}")

            # Всего часов фактически
            hours_of_total_actually = educational_work_data[f'Q{row}'].value
            if hours_of_total_actually is None:
                hours_of_total_actually = 0
            Rich.debug_log(f"Всего часов фактически: {hours_of_total_actually}")

            data_of_disciplines_in_semester = InformationOnDisciplineOfAcademicWork(
                name_of_discipline = subject_name,
                group = current_group,
                number_of_semester = educational_semester,
                lectures = hours_of_lectures,
                practical_training = hours_of_practice_lessons,
                laboratory_work = hours_of_laboratory_work,
                consultations = hours_of_consultations,
                exams = hours_of_exams,
                credits = hours_of_credits,
                term_papers_and_works = hours_of_terms_works,
                practice = hours_of_practice,
                WRC = hours_WRC,
                GEK = hours_of_GEC,
                additional_work = hours_of_additional_works,
                total_according_plan = hours_of_total_according_to_plan,
                total_actually = hours_of_total_actually
            )

            list_of_disciplines_in_semester.append(data_of_disciplines_in_semester)

        total_hours_of_lectures = -1.0
        total_hours_of_practice_lessons = -1.0
        total_hours_of_laboratory_work = -1.0
        total_hours_of_consultations = -1.0
        total_hours_of_exams = -1.0
        total_hours_of_credits = -1.0
        total_hours_of_terms_works = -1.0
        total_hours_of_practice = -1.0
        total_hours_WRC = -1.0
        total_hours_of_GEC = -1.0
        total_hours_of_additional_works = -1.0
        total_hours_of_total_according_to_plan = -1.0
        total_hours_of_total_actually = -1.0

        summary_data_of_hours_in_semester = TeachersSummaryInfoOnHoursOfWorkPerSemester(
            summary_lectures = total_hours_of_lectures,
            summary_practical_training = total_hours_of_practice_lessons,
            summary_laboratory_work = total_hours_of_laboratory_work,
            summary_consultations = total_hours_of_consultations,
            summary_exams = total_hours_of_exams,
            summary_credits = total_hours_of_credits,
            summary_term_papers_and_works = total_hours_of_terms_works,
            summary_practice = total_hours_of_practice,
            summary_WRC = total_hours_WRC,
            summary_GEK = total_hours_of_GEC,
            summary_additional_work = total_hours_of_additional_works,
            summary_total_according_plan = total_hours_of_total_according_to_plan,
            summary_total_actually = total_hours_of_total_actually
        )

        if (not educational_work_data[f'A{row}'].value is None
                and "Итого за семестр" in educational_work_data[f'A{row}'].value):
            # Количество часов лекций - итог
            total_hours_of_lectures = educational_work_data[f'E{row}'].value
            if total_hours_of_lectures is None:
                total_hours_of_lectures = 0
            Rich.debug_log(f"Итоговое количество часов "
                           f"лекций: {total_hours_of_lectures}")

            # Количество часов практик - итог
            total_hours_of_practice_lessons = educational_work_data[f'F{row}'].value
            if total_hours_of_practice_lessons is None:
                total_hours_of_practice_lessons = 0
            Rich.debug_log(f"Итоговое количество часов "
                           f"практики: {total_hours_of_practice_lessons}")

            # Количество часов лабораторных работ - итог
            total_hours_of_laboratory_work = educational_work_data[f'G{row}'].value
            if total_hours_of_laboratory_work is None:
                total_hours_of_laboratory_work = 0
            Rich.debug_log(f"Итоговое количество часов "
                           f"лабораторных работ: {total_hours_of_laboratory_work}")

            # Количество часов консультаций - итог
            total_hours_of_consultations = educational_work_data[f'H{row}'].value
            if total_hours_of_consultations is None:
                total_hours_of_consultations = 0
            Rich.debug_log(f"Итоговое количество часов "
                           f"консультаций: {total_hours_of_consultations}")

            # Часов экзаменов - итог
            total_hours_of_exams = educational_work_data[f'I{row}'].value
            if total_hours_of_exams is None:
                total_hours_of_exams = 0
            Rich.debug_log(f"Итоговое количество часов "
                           f"экзаменов: {total_hours_of_exams}")

            # Часов зачётов - итог
            total_hours_of_credits = educational_work_data[f'J{row}'].value
            if total_hours_of_credits is None:
                total_hours_of_credits = 0
            Rich.debug_log(f"Итоговое количество часов "
                           f"зачётов: {total_hours_of_credits}")

            # Часов курсовых работ, курсовых проектов - итог
            total_hours_of_terms_works = educational_work_data[f'K{row}'].value
            if total_hours_of_terms_works is None:
                total_hours_of_terms_works = 0
            Rich.debug_log(f"Итоговое количество часов курсовых работ, курсовых "
                           f"проектов: {total_hours_of_terms_works}")

            # Часов практики - итог
            total_hours_of_practice = educational_work_data[f'L{row}'].value
            if total_hours_of_practice is None:
                total_hours_of_practice = 0
            Rich.debug_log(f"Итоговое количество часов практики: {total_hours_of_practice}")

            # Часов ВКП - итог
            total_hours_WRC = educational_work_data[f'M{row}'].value
            if total_hours_WRC is None:
                total_hours_WRC = 0
            Rich.debug_log(f"Итоговое количество часов ВКР: {total_hours_WRC}")

            # Часов ГЭК - итог
            total_hours_of_GEC = educational_work_data[f'N{row}'].value
            if total_hours_of_GEC is None:
                total_hours_of_GEC = 0
            Rich.debug_log(f"Итоговое количество часов ГЭК: {total_hours_of_GEC}")

            # Часов дополнительных работ - итог
            total_hours_of_additional_works = educational_work_data[f'O{row}'].value
            if total_hours_of_additional_works is None:
                total_hours_of_additional_works = 0
            Rich.debug_log(f"Итоговое количество часов "
                           f"дополнительных работ: {total_hours_of_additional_works}")

            # Всего часов по плану - итог
            total_hours_of_total_according_to_plan = educational_work_data[f'P{row}'].value
            if total_hours_of_total_according_to_plan is None:
                total_hours_of_total_according_to_plan = 0
            Rich.debug_log(f"Итоговое количество часов "
                           f"по плану: {total_hours_of_total_according_to_plan}")

            # Всего часов фактически - итог
            total_hours_of_total_actually = educational_work_data[f'Q{row}'].value
            if total_hours_of_total_actually is None:
                total_hours_of_total_actually = 0
            Rich.debug_log(f"Итоговое количество "
                           f"часов фактически: {total_hours_of_total_actually}")

            data_of_summary_hours_of_disciplines_in_semester = TeachersSummaryInfoOnHoursOfWorkPerSemester(
                summary_lectures = total_hours_of_lectures,
                summary_practical_training = total_hours_of_practice_lessons,
                summary_laboratory_work = total_hours_of_laboratory_work,
                summary_consultations = total_hours_of_consultations,
                summary_exams = total_hours_of_exams,
                summary_credits = total_hours_of_credits,
                summary_term_papers_and_works = total_hours_of_terms_works,
                summary_practice = total_hours_of_practice,
                summary_WRC = total_hours_WRC,
                summary_GEK = total_hours_of_GEC,
                summary_additional_work = total_hours_of_additional_works,
                summary_total_according_plan = total_hours_of_total_according_to_plan,
                summary_total_actually = total_hours_of_total_actually
            )
            summary_data_of_hours_in_semester = data_of_summary_hours_of_disciplines_in_semester

            data_of_semester = TeacherAcademicWorkPerSemester (
                semester = current_semester,
                disciplines = list_of_disciplines_in_semester,
                summary_data_of_hours = summary_data_of_hours_in_semester
            )

            list_with_semesters_data.append(data_of_semester)
            Rich.debug_log(f"Записана информация о {current_semester}")
