import re
from typing import List

from openpyxl import load_workbook, Workbook

from parser.itp_models import (
    InfoFromTitlePage,
    TeacherGeneralInfo,
    DataNamesOfWorksFromSummaryInfo,
    TeacherSummaryInfo,
    InformationOnDisciplineOfAcademicWork,
    TeachersSummaryInfoOnHoursOfWorkPerSemester,
    TeacherAcademicWorkPerSemester,
    FullInfoOnEducationWorkOfTeacher,
    SummaryInfoOnHoursOfTeachersAcademicWork,
    RowData,
    TeacherEducationalAndMethodicalWorkData,
    TeacherScientificAndResearchInfo,
    TeacherOrgAndPedagogicalInfo,
    RowDataProfessionalDevelopment,
    TeachersProfessionalDevelopmentInfo,
    TeachersAdditionalWorkData,
    FullITP)
from utils.output_rich import Rich
from utils.utils_funcs import get_path_resources_file


class ParserITP:
    """
    Класс-обёртка для функций парсинга данных из таблицы индивидуального плана работы
     преподавателя на openpyxl.

    Содержит статические методы для парсинга отдельных страниц таблицы индивидуального
     плана работы преподавателя и функция для парсинга сразу всех страниц.

    Для выгрузки данных использую методы из core/data_keeper.py, который выгрузает
     данные парсинга в json словари

    Содержит функции для парсинга отдельных листов таблицы:
    * Общие сведения
    * Сводные данные
    * листы 1. , 1.1, 1.2, 2, 3, 4

    Парсит все листы, кроме листа "Закл.".

    Работает с моделями из core/models.py, сохраняя полученные данные в объекты датаклассав.
    """

    list_with_semesters_data: List[TeacherAcademicWorkPerSemester] = []
    """Вспомогательный массив для хранения информации по дисциплинам 
    из функции парсинга учебной работы преподавателя"""

    list_with_data_of_teachers_additional_work: List[InformationOnDisciplineOfAcademicWork] = []
    """Вспомогательный массив для хранения всех дисциплин, по которым у преподавателя 
    есть дополнительная нагрузка
    """

    @staticmethod
    def rounding(number: float) -> float:
        """
        Метод для округления числа до десятых
        :param number: принимает вещественное число
        :return: возвращает округлённое вещественное число
        """
        return round(float(number), 1)

    @staticmethod
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

    @staticmethod
    def parse_title_sheet(file_path: str) -> InfoFromTitlePage:
        """
        Функция для парсинга титульного листа таблицы ИПРП

        :param file_path: путь к таблице ИПРП

        :return: InfoFromTitlePage - объект датакласса с информацией из титульного листа
        """
        individual_plan = ParserITP.load_table(get_path_resources_file(file_path))
        # Открываю титульный лист
        tit_list_info = individual_plan["Тит. лист"]
        Rich.simple_log(f"Индивидуальный лист работы преподавателя")
        Rich.print_spacer()

        # парсинг

        # год создания документа
        year_doc_created = tit_list_info['D49'].value
        Rich.simple_log(f"Год составления документа: {year_doc_created}")

        # рассмотрено на заседании - дата
        date_of_meeting = tit_list_info['A16'].value
        Rich.debug_log(f"Рассмотрено на заседании: {date_of_meeting}")

        # номер протокола заседания
        number_of_protocol_of_meeting = tit_list_info['A17'].value
        Rich.debug_log(f"Номер протокола заседания: {number_of_protocol_of_meeting}")

        # кем утверждено
        who_approved = tit_list_info['F16'].value.strip()
        Rich.debug_log(f"Кем утверждено: {who_approved}")

        # дата утверждения ИПРП
        date_of_approved = tit_list_info['F17'].value
        Rich.debug_log(f"Дата утверждения ИПРП: {date_of_approved}")

        # кафедра
        department = tit_list_info['A25'].value
        Rich.debug_log(f"Кафедра: {department}")

        # институт
        institute = tit_list_info['A28'].value
        Rich.debug_log(f"Институт: {institute}")

        # фио
        teachers_fio = tit_list_info['A31'].value
        Rich.debug_log(f"ФИО преподавателя: {teachers_fio}")

        # наименование должности
        name_of_position = tit_list_info['A34'].value
        Rich.debug_log(f"Наименование должности: {name_of_position}")

        # на какой год ИПРП
        year_of_plan = tit_list_info['A37'].value
        Rich.debug_log(f"ИПРП на год: {year_of_plan}")

        title_list_information = InfoFromTitlePage(
            year_doc_created=year_doc_created,
            date_of_meeting=date_of_meeting,
            number_of_protocol_of_meeting=number_of_protocol_of_meeting,
            who_approved=who_approved,
            date_of_approved=date_of_approved,
            department=department,
            institute=institute,
            teachers_fio=teachers_fio,
            name_of_position=name_of_position,
            year_of_plan=year_of_plan
        )
        Rich.simple_log("Получена информация из титульного листа ИПРП")

        return title_list_information

    @staticmethod
    def parse_general_info_sheet(
            file_path: str) -> TeacherGeneralInfo:
        """
        Парсинг данных с листа "Общие сведения"
        из таблицы индивидуального плана преподавателя

        :param file_path: путь к таблице ИПРП

        :return: TeacherGeneralInfo - вернёт объект с полученными данными
        """
        individual_plan = ParserITP.load_table(get_path_resources_file(file_path))
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
            Rich.debug_log(f"Учёное звание: {teacher_academic_title}")

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
            name = teacher_name,
            post = teacher_post,
            amount_of_bet = teacher_amount_of_bet,
            terms_of_attraction = teacher_terms_of_attraction,
            academic_degree = teacher_academic_degree,
            academic_title = teacher_academic_title,
            # Сведения о контракте
            date_and_number = teacher_data_and_number,
            validity_period = teacher_validity_period,
            basic_education = teacher_basic_education,
            name_educational_program = teacher_name_educational_program,
            qualification = teacher_qualification,
            list_subjects_taught = teacher_list_subjects_taught
        )

        Rich.print_spacer()

        return parsed_data

    @staticmethod
    def parse_summary_data_sheet(file_path: str) -> TeacherSummaryInfo:
        """
        Функция для паргинга листа "Сводные данные" из таблицы ИПРП

        :param file_path: путь к файлу таблицы ИПРП

        :return: TeacherSummaryInfo - возвращает объект с полученными данными
        """
        individual_plan = ParserITP.load_table(get_path_resources_file(file_path))
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
                    teachers_total_number_of_hours = ParserITP.rounding(
                        iter_cell_with_number_of_hours)
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

        Rich.print_spacer()

        return summary_data_from_table

    @staticmethod
    def parse_educational_work_sheet(
            file_path: str) -> FullInfoOnEducationWorkOfTeacher:
        """
        Функция для парсинга листа 1.1 "Учебная работа" из талицы ИПП для получения
        информации о дисциплинах, типах занятий, количестве часов, группах и
        другой информации по учебной работе преподавателя.

        :param file_path: путь к файлу таблицы ИПРП

        :return: FullInfoOnEducationWorkOfTeacher - объект с полученными данными
        """
        individual_plan = ParserITP.load_table(get_path_resources_file(file_path))
        # Открываю лист с учебной работой - лист 1.1.
        educational_work_data = individual_plan["1.1. "]
        Rich.print_spacer()
        # Вывод шапки листа
        Rich.simple_log(" ".join((educational_work_data['A1'].value).split()))

        current_semester = ""
        current_group = ""

        list_of_disciplines_in_semester: List[InformationOnDisciplineOfAcademicWork] = []

        for row in range(5, educational_work_data.max_row - 2):
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
                    current_semester = " ".join(current_semester.split())
                    current_semester = re.sub(
                        r"^[а-яёa-z]\s*\)\s*",
                        "",
                        current_semester,
                        flags=re.IGNORECASE)
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
                hours_of_lectures = ParserITP.rounding(hours_of_lectures)
                Rich.debug_log(f"Часов лекций: {hours_of_lectures}")

                # Количество часов практики
                hours_of_practice_lessons = educational_work_data[f'F{row}'].value
                if  hours_of_practice_lessons is None:
                    hours_of_practice_lessons = 0
                hours_of_practice_lessons = ParserITP.rounding(hours_of_practice_lessons)
                Rich.debug_log(f"Часов практики: {hours_of_practice_lessons}")

                # Количество часов лабораторных работ
                hours_of_laboratory_work = educational_work_data[f'G{row}'].value
                if hours_of_laboratory_work is None:
                    hours_of_laboratory_work = 0
                hours_of_laboratory_work = ParserITP.rounding(hours_of_laboratory_work)
                Rich.debug_log(f"Часов лабораторных работ: {hours_of_laboratory_work}")

                # Количество часов консультаций
                hours_of_consultations = educational_work_data[f'H{row}'].value
                if hours_of_consultations is None:
                    hours_of_consultations = 0
                hours_of_consultations = round(float(hours_of_consultations),1)
                Rich.debug_log(f"Часов консультаций: {hours_of_consultations}")

                # Часов экзаменов
                hours_of_exams = educational_work_data[f'I{row}'].value
                if hours_of_exams is None:
                    hours_of_exams = 0
                hours_of_exams = round(float(hours_of_exams), 1)
                Rich.debug_log(f"Часов экзаменов: {hours_of_exams}")

                # Часов зачётов
                hours_of_credits = educational_work_data[f'J{row}'].value
                if hours_of_credits is None:
                    hours_of_credits = 0
                hours_of_credits = ParserITP.rounding(hours_of_credits)
                Rich.debug_log(f"Часов зачётов: {hours_of_credits}")

                # Часов курсовых работ, курсовых проектов
                hours_of_terms_works = educational_work_data[f'K{row}'].value
                if hours_of_terms_works is None:
                    hours_of_terms_works = 0
                hours_of_terms_works = ParserITP.rounding(hours_of_terms_works)
                Rich.debug_log(f"Часов курсовых работ, курсовых проектов: {hours_of_terms_works}")

                # Часов практики
                hours_of_practice = educational_work_data[f'L{row}'].value
                if hours_of_practice is None:
                    hours_of_practice = 0
                hours_of_practice = ParserITP.rounding(hours_of_practice)
                Rich.debug_log(f"Часов практики: {hours_of_practice}")

                # Часов ВКП
                hours_WRC = educational_work_data[f'M{row}'].value
                if hours_WRC is None:
                    hours_WRC = 0
                hours_WRC = ParserITP.rounding(hours_WRC)
                Rich.debug_log(f"Часов ВКР: {hours_WRC}")

                # Часов ГЭК
                hours_of_GEC = educational_work_data[f'N{row}'].value
                if hours_of_GEC is None:
                    hours_of_GEC = 0
                hours_of_GEC = ParserITP.rounding(hours_of_GEC)
                Rich.debug_log(f"Часов ГЭК: {hours_of_GEC}")

                # Часов дополнительных работ
                hours_of_additional_works = educational_work_data[f'O{row}'].value
                if hours_of_additional_works is None:
                    hours_of_additional_works = 0
                hours_of_additional_works = ParserITP.rounding(hours_of_additional_works)
                Rich.debug_log(f"Часов дополнительных работ: {hours_of_additional_works}")

                # Всего часов по плану
                hours_of_total_according_to_plan = educational_work_data[f'P{row}'].value
                if hours_of_total_according_to_plan is None:
                    hours_of_total_according_to_plan = 0
                hours_of_total_according_to_plan = round(float(hours_of_total_according_to_plan),1)
                Rich.debug_log(f"Всего часов по плану: {hours_of_total_according_to_plan}")

                # Всего часов фактически
                hours_of_total_actually = educational_work_data[f'Q{row}'].value
                if hours_of_total_actually is None:
                    hours_of_total_actually = 0
                hours_of_total_actually = ParserITP.rounding(hours_of_total_actually)
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

            # Получение итоговой информации по часам
            if (not educational_work_data[f'A{row}'].value is None
                    and "Итого за семестр" in educational_work_data[f'A{row}'].value):

                # Количество часов лекций - итог
                total_hours_of_lectures = educational_work_data[f'E{row}'].value
                if total_hours_of_lectures is None:
                    total_hours_of_lectures = 0
                total_hours_of_lectures = ParserITP.rounding(total_hours_of_lectures)
                Rich.debug_log(f"Итоговое количество часов "
                               f"лекций: {total_hours_of_lectures}")

                # Количество часов практик - итог
                total_hours_of_practice_lessons = educational_work_data[f'F{row}'].value
                if total_hours_of_practice_lessons is None:
                    total_hours_of_practice_lessons = 0
                total_hours_of_practice_lessons = ParserITP.rounding(
                    total_hours_of_practice_lessons)
                Rich.debug_log(f"Итоговое количество часов "
                               f"практики: {total_hours_of_practice_lessons}")

                # Количество часов лабораторных работ - итог
                total_hours_of_laboratory_work = educational_work_data[f'G{row}'].value
                if total_hours_of_laboratory_work is None:
                    total_hours_of_laboratory_work = 0
                total_hours_of_laboratory_work = ParserITP.rounding(
                    total_hours_of_laboratory_work)
                Rich.debug_log(f"Итоговое количество часов "
                               f"лабораторных работ: {total_hours_of_laboratory_work}")

                # Количество часов консультаций - итог
                total_hours_of_consultations = educational_work_data[f'H{row}'].value
                if total_hours_of_consultations is None:
                    total_hours_of_consultations = 0
                total_hours_of_consultations = ParserITP.rounding(
                    total_hours_of_consultations)
                Rich.debug_log(f"Итоговое количество часов "
                               f"консультаций: {total_hours_of_consultations}")

                # Часов экзаменов - итог
                total_hours_of_exams = educational_work_data[f'I{row}'].value
                if total_hours_of_exams is None:
                    total_hours_of_exams = 0
                total_hours_of_exams = ParserITP.rounding(total_hours_of_exams)
                Rich.debug_log(f"Итоговое количество часов "
                               f"экзаменов: {total_hours_of_exams}")

                # Часов зачётов - итог
                total_hours_of_credits = educational_work_data[f'J{row}'].value
                if total_hours_of_credits is None:
                    total_hours_of_credits = 0
                total_hours_of_credits = ParserITP.rounding(total_hours_of_credits)
                Rich.debug_log(f"Итоговое количество часов "
                               f"зачётов: {total_hours_of_credits}")

                # Часов курсовых работ, курсовых проектов - итог
                total_hours_of_terms_works = educational_work_data[f'K{row}'].value
                if total_hours_of_terms_works is None:
                    total_hours_of_terms_works = 0
                total_hours_of_terms_works = ParserITP.rounding(
                    total_hours_of_terms_works)
                Rich.debug_log(f"Итоговое количество часов курсовых работ, курсовых "
                               f"проектов: {total_hours_of_terms_works}")

                # Часов практики - итог
                total_hours_of_practice = educational_work_data[f'L{row}'].value
                if total_hours_of_practice is None:
                    total_hours_of_practice = 0
                total_hours_of_practice = ParserITP.rounding(total_hours_of_practice)
                Rich.debug_log(f"Итоговое количество часов практики: "
                               f"{total_hours_of_practice}")

                # Часов ВКП - итог
                total_hours_WRC = educational_work_data[f'M{row}'].value
                if total_hours_WRC is None:
                    total_hours_WRC = 0
                total_hours_WRC = ParserITP.rounding(total_hours_WRC)
                Rich.debug_log(f"Итоговое количество часов ВКР: "
                               f"{total_hours_WRC}")

                # Часов ГЭК - итог
                total_hours_of_GEC = educational_work_data[f'N{row}'].value
                if total_hours_of_GEC is None:
                    total_hours_of_GEC = 0
                total_hours_of_GEC = ParserITP.rounding(total_hours_of_GEC)
                Rich.debug_log(f"Итоговое количество часов ГЭК: {total_hours_of_GEC}")

                # Часов дополнительных работ - итог
                total_hours_of_additional_works = educational_work_data[f'O{row}'].value
                if total_hours_of_additional_works is None:
                    total_hours_of_additional_works = 0
                total_hours_of_additional_works = ParserITP.rounding(total_hours_of_additional_works)
                Rich.debug_log(f"Итоговое количество часов "
                               f"дополнительных работ: "
                               f"{total_hours_of_additional_works}")

                # Всего часов по плану - итог
                total_hours_of_total_according_to_plan = educational_work_data[f'P{row}'].value
                if total_hours_of_total_according_to_plan is None:
                    total_hours_of_total_according_to_plan = 0
                total_hours_of_total_according_to_plan = ParserITP.rounding(
                    total_hours_of_total_according_to_plan)
                Rich.debug_log(f"Итоговое количество часов "
                               f"по плану: {total_hours_of_total_according_to_plan}")

                # Всего часов фактически - итог
                total_hours_of_total_actually = educational_work_data[f'Q{row}'].value
                if total_hours_of_total_actually is None:
                    total_hours_of_total_actually = 0
                total_hours_of_total_actually = ParserITP.rounding(
                    total_hours_of_total_actually)
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
                    summary_data_of_hours_by_semester = summary_data_of_hours_in_semester
                )

                ParserITP.list_with_semesters_data.append(data_of_semester)
                Rich.simple_log(f"Записана информация о {current_semester}")

        num_row_total_info_hours_educational_work_for_year = educational_work_data.max_row - 1

        # Количество часов лекций - итог за год
        total_hours_of_lectures_by_year = educational_work_data[
            f'E{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_of_lectures_by_year is None:
            total_hours_of_lectures_by_year = 0
        total_hours_of_lectures_by_year = ParserITP.rounding(
            total_hours_of_lectures_by_year)
        Rich.debug_log(f"Итоговое количество часов "
                       f"лекций за год: "
                       f"{total_hours_of_lectures_by_year}")

        # Количество часов практик - итог за год
        total_hours_of_practice_lessons_by_year = educational_work_data[
            f'F{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_of_practice_lessons_by_year is None:
            total_hours_of_practice_lessons_by_year = 0
        total_hours_of_practice_lessons_by_year = ParserITP.rounding(
            total_hours_of_practice_lessons_by_year)
        Rich.debug_log(f"Итоговое количество часов "
                       f"практики за год: "
                       f"{total_hours_of_practice_lessons_by_year}")

        # Количество часов лабораторных работ - итог за год
        total_hours_of_laboratory_work_by_year = educational_work_data[
            f'G{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_of_laboratory_work_by_year is None:
            total_hours_of_laboratory_work_by_year = 0
        total_hours_of_laboratory_work_by_year = ParserITP.rounding(
            total_hours_of_laboratory_work_by_year)
        Rich.debug_log(f"Итоговое количество часов "
                       f"лабораторных работ за год: "
                       f"{total_hours_of_laboratory_work_by_year}")

        # Количество часов консультаций - итог за год
        total_hours_of_consultations_by_year = educational_work_data[
            f'H{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_of_consultations_by_year is None:
            total_hours_of_consultations_by_year = 0
        total_hours_of_consultations_by_year = ParserITP.rounding(
            total_hours_of_consultations_by_year)
        Rich.debug_log(f"Итоговое количество часов "
                       f"консультаций за год: "
                       f"{total_hours_of_consultations_by_year}")

        # Часов экзаменов - итог за год
        total_hours_of_exams_by_year = educational_work_data[
            f'I{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_of_exams_by_year is None:
            total_hours_of_exams_by_year = 0
        total_hours_of_exams_by_year = ParserITP.rounding(
            total_hours_of_exams_by_year)
        Rich.debug_log(f"Итоговое количество часов "
                       f"экзаменов за год: {total_hours_of_exams_by_year}")

        # Часов зачётов - итог за год
        total_hours_of_credits_by_year = educational_work_data[
            f'J{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_of_credits_by_year is None:
            total_hours_of_credits_by_year = 0
        total_hours_of_credits_by_year = ParserITP.rounding(
            total_hours_of_credits_by_year)
        Rich.debug_log(f"Итоговое количество часов "
                       f"зачётов за год: {total_hours_of_credits_by_year}")

        # Часов курсовых работ, курсовых проектов - итог за год
        total_hours_of_terms_works_by_year = educational_work_data[
            f'K{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_of_terms_works_by_year is None:
            total_hours_of_terms_works_by_year = 0
        total_hours_of_terms_works_by_year = ParserITP.rounding(
            total_hours_of_terms_works_by_year)
        Rich.debug_log(f"Итоговое количество часов курсовых работ, курсовых "
                       f"проектов за год: {total_hours_of_terms_works_by_year}")

        # Часов практики - итог за год
        total_hours_of_practice_by_year = educational_work_data[
            f'L{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_of_practice_by_year is None:
            total_hours_of_practice_by_year = 0
        total_hours_of_practice_by_year = ParserITP.rounding(
            total_hours_of_practice_by_year)
        Rich.debug_log(f"Итоговое количество часов практики за год: "
                       f"{total_hours_of_practice_by_year}")

        # Часов ВКП - итог за год
        total_hours_WRC_by_year = educational_work_data[
            f'M{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_WRC_by_year is None:
            total_hours_WRC_by_year = 0
        total_hours_WRC_by_year = ParserITP.rounding(
            total_hours_WRC_by_year)
        Rich.debug_log(f"Итоговое количество часов ВКР за год: "
                       f"{total_hours_WRC_by_year}")

        # Часов ГЭК - итог за год
        total_hours_of_GEC_by_year = educational_work_data[
            f'N{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_of_GEC_by_year is None:
            total_hours_of_GEC_by_year = 0
        total_hours_of_GEC_by_year = ParserITP.rounding(
            total_hours_of_GEC_by_year)
        Rich.debug_log(f"Итоговое количество часов ГЭК за год: "
                       f"{total_hours_of_GEC_by_year}")

        # Часов дополнительных работ - итог за год
        total_hours_of_additional_works_by_year = educational_work_data[
            f'O{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_of_additional_works_by_year is None:
            total_hours_of_additional_works_by_year = 0
        total_hours_of_additional_works_by_year = ParserITP.rounding(
            total_hours_of_additional_works_by_year)
        Rich.debug_log(f"Итоговое количество часов "
                       f"дополнительных работ за год: "
                       f"{total_hours_of_additional_works_by_year}")

        # Всего часов по плану - итог за год
        total_hours_of_total_according_to_plan_by_year = educational_work_data[
            f'P{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_of_total_according_to_plan_by_year is None:
            total_hours_of_total_according_to_plan_by_year = 0
        total_hours_of_total_according_to_plan_by_year = ParserITP.rounding(
            total_hours_of_total_according_to_plan_by_year)
        Rich.debug_log(f"Итоговое количество часов "
                       f"по плану за год: "
                       f"{total_hours_of_total_according_to_plan_by_year}")

        # Всего часов фактически - итог за год
        total_hours_of_total_actually_by_year = educational_work_data[
            f'Q{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_of_total_actually_by_year is None:
            total_hours_of_total_actually_by_year = 0
        total_hours_of_total_actually_by_year = ParserITP.rounding(
            total_hours_of_total_actually_by_year)
        Rich.debug_log(f"Итоговое количество "
                       f"часов фактически за год: "
                       f"{total_hours_of_total_actually_by_year}")

        summary_data_of_hours_teachers_educational_work_by_year = SummaryInfoOnHoursOfTeachersAcademicWork(
            summary_lectures_per_year = total_hours_of_lectures_by_year,
            summary_practical_training_per_year = total_hours_of_practice_lessons_by_year,
            summary_laboratory_work_per_year = total_hours_of_laboratory_work_by_year,
            summary_consultations_per_year = total_hours_of_consultations_by_year,
            summary_exams_per_year = total_hours_of_exams_by_year,
            summary_credits_per_year = total_hours_of_credits_by_year,
            summary_term_papers_and_works_per_year = total_hours_of_terms_works_by_year,
            summary_practice_per_year = total_hours_of_practice_by_year,
            summary_WRC_per_year = total_hours_WRC_by_year,
            summary_GEK_per_year = total_hours_of_GEC_by_year,
            summary_additional_work_per_year = total_hours_of_additional_works_by_year,
            summary_total_according_plan_per_year = total_hours_of_total_according_to_plan_by_year,
            summary_total_actually = total_hours_of_total_actually_by_year
        )

        autumn_semester = -1
        spring_semester = -1

        if len(ParserITP.list_with_semesters_data) == 2:
            autumn_semester = ParserITP.list_with_semesters_data[0]
            spring_semester = ParserITP.list_with_semesters_data[1]
            Rich.success_log("Информация по семестрам получена")
        else:
            Rich.warning_log("Не удалось получить информацию по семестрам")

        teachers_educational_work = FullInfoOnEducationWorkOfTeacher(
            autumn_semester = autumn_semester,
            spring_semester = spring_semester,
            summary_info_about_educational_work_by_year = summary_data_of_hours_teachers_educational_work_by_year
        )

        Rich.success_log("Добавлена информация о учебной работе преподавателя")
        ParserITP.list_with_semesters_data.clear()

        return teachers_educational_work

    @staticmethod
    def parse_educational_and_methodical_work_sheet(
            file_path: str) -> TeacherEducationalAndMethodicalWorkData:
        """
        Функция для парсинга листа 1.2 таблицы ИПП. Парсит лист с учебно-методической работой
        :param file_path: путь к файлу таблицы ИПП
        :return: TeacherEducationalAndMethodicalWorkData - объект с полученными данными
        """
        individual_plan = ParserITP.load_table(get_path_resources_file(file_path))
        # Открываю лист с учебно-методической работой - лист 1.2.
        educational_and_methodical_data = individual_plan["1.2."]
        Rich.print_spacer()
        # Вывод шапки листа
        Rich.simple_log(" ".join((educational_and_methodical_data['B1'].value).split()))

        # Начало парсинга данных

        # Общий объём планируемой учебно-методической работы за учебный год, часов
        total_amount_of_planned_educational_and_methodological_work_for_academic_year = (
            float(educational_and_methodical_data['E3'].value)
        )
        Rich.debug_log(f"Общий объём планируемой учебно-методической работы за учебный год, часов: {
            total_amount_of_planned_educational_and_methodological_work_for_academic_year
        }")

        list_of_types_of_jobs: List[RowData] = []

        for row in range(7, educational_and_methodical_data.max_row - 1):
            if not educational_and_methodical_data[f'B{row}'].value is None:
                # Наименование вида работы
                name_of_work = educational_and_methodical_data[f'B{row}'].value
                Rich.debug_log(f"Вид работы: {name_of_work}")

                # Трудоёмкость, часов
                number_of_hours = float(educational_and_methodical_data[f'C{row}'].value)
                Rich.debug_log(f"Трудоёмкость, часов: {number_of_hours}")

                # Срок выполнения (месяц, год)
                period_of_execution = educational_and_methodical_data[f'D{row}'].value.date().strftime("%d.%m.%Y")
                Rich.debug_log(f"Срок выполнения (месяц, год): {period_of_execution}")

                # Отметка о выполнении
                mark_of_completion = educational_and_methodical_data[f'E{row}'].value
                Rich.debug_log(f"Отметка о выполнении: {mark_of_completion}")

                row_data = RowData(
                    work_name = name_of_work,
                    number_of_hours_for_work = number_of_hours,
                    period_of_execution_for_work = period_of_execution
                )

                list_of_types_of_jobs.append(row_data)

        education_and_methodical_info = TeacherEducationalAndMethodicalWorkData(
            total_hours = total_amount_of_planned_educational_and_methodological_work_for_academic_year,
            list_of_data_with_jobs = list_of_types_of_jobs
        )

        Rich.debug_log("Получена информация о учебно-методической работе преподавателя")
        Rich.debug_log(f"Всего работ: {len(list_of_types_of_jobs)}")

        return education_and_methodical_info

    @staticmethod
    def parse_scientific_research_activities_sheet(
            file_path: str) -> TeacherScientificAndResearchInfo:
        """
        Функция для парсинга листа 2 таблицы ИПРП. Парсит лист с научно-исследовательской
         деятельностью

        :param file_path: путь к файлу таблицы ИПРП

        :return: TeacherScientificAndResearchInfo - объект с полученными данными
        """
        individual_plan = ParserITP.load_table(get_path_resources_file(file_path))
        # Открываю лист с научно-исследовательской работой - лист 2
        scientific_and_research_data = individual_plan["2"]
        Rich.print_spacer()
        # Вывод шапки листа
        Rich.simple_log(" ".join((scientific_and_research_data['A1'].value).split()))

        # Начало парсинга данных

        # Общий объём планируемой научно-исследовательской деятельности за учебный год
        total_amount_of_planned_educational_and_methodological_work_for_academic_year = (
            float(scientific_and_research_data['E3'].value)
        )
        Rich.debug_log(f"Общий объём планируемой работы за учебный год, часов: {
            total_amount_of_planned_educational_and_methodological_work_for_academic_year
        }")

        list_of_types_of_jobs: List[RowData] = []

        for row in range(7, scientific_and_research_data.max_row - 1):
            if not scientific_and_research_data[f'B{row}'].value is None:
                # Наименование вида работы
                name_of_work = scientific_and_research_data[f'B{row}'].value
                Rich.debug_log(f"Вид работы: {name_of_work}")

                # Трудоёмкость, часов
                number_of_hours = float(scientific_and_research_data[f'C{row}'].value)
                Rich.debug_log(f"Трудоёмкость, часов: {number_of_hours}")

                # Срок выполнения (месяц, год)
                period_of_execution = scientific_and_research_data[f'D{row}'].value.date().strftime("%d.%m.%Y")
                Rich.debug_log(f"Срок выполнения (месяц, год): {period_of_execution}")

                # Отметка о выполнении
                mark_of_completion = scientific_and_research_data[f'E{row}'].value
                Rich.debug_log(f"Отметка о выполнении: {mark_of_completion}")

                row_data = RowData(
                    work_name = name_of_work,
                    number_of_hours_for_work = number_of_hours,
                    period_of_execution_for_work = period_of_execution
                )

                list_of_types_of_jobs.append(row_data)

        scientific_and_research_info = TeacherScientificAndResearchInfo(
            total_hours = total_amount_of_planned_educational_and_methodological_work_for_academic_year,
            list_of_data_with_jobs = list_of_types_of_jobs
        )

        Rich.debug_log("Получена информация о научно-исследовательской работе преподавателя")
        Rich.debug_log(f"Всего работ: {len(list_of_types_of_jobs)}")

        return scientific_and_research_info

    @staticmethod
    def parse_organizational_and_pedagogical_activities_sheet(
            file_path: str) -> TeacherOrgAndPedagogicalInfo:
        """
        Функция для парсинга информации по организационной и воспитательной деятельности
        преподавателя.
        Информация берётся из листа 3 таблицы ИПРП

        :param file_path: путь к файлу таблицы ИПРП
        :return: TeacherOrgAndPedagogicalInfo - объект с полученными данными
        """
        individual_plan = ParserITP.load_table(get_path_resources_file(file_path))
        # Открываю лист с организационно-воспитательной работой - лист 3
        org_and_pedagogical_data = individual_plan["3"]
        Rich.print_spacer()
        # Вывод шапки листа
        Rich.simple_log(" ".join((org_and_pedagogical_data['A1'].value).split()))

        # Начало парсинга данных

        # Общий объём планируемой организационной и воспитательной работы за учебный год
        total_amount_of_planned_educational_and_methodological_work_for_academic_year = (
            float(org_and_pedagogical_data['E3'].value)
        )
        Rich.debug_log(f"Общий объём планируемой работы за учебный год, часов: {
        total_amount_of_planned_educational_and_methodological_work_for_academic_year
        }")

        list_of_types_of_jobs: List[RowData] = []

        for row in range(7, org_and_pedagogical_data.max_row - 1):
            if not org_and_pedagogical_data[f'B{row}'].value is None:
                # Наименование вида работы
                name_of_work = org_and_pedagogical_data[f'B{row}'].value
                Rich.debug_log(f"Вид работы: {name_of_work}")

                # Трудоёмкость, часов
                number_of_hours = float(org_and_pedagogical_data[f'C{row}'].value)
                Rich.debug_log(f"Трудоёмкость, часов: {number_of_hours}")

                # Срок выполнения (месяц, год)
                period_of_execution = org_and_pedagogical_data[f'D{row}'].value.date().strftime("%d.%m.%Y")
                Rich.debug_log(f"Срок выполнения (месяц, год): {period_of_execution}")

                # Отметка о выполнении
                mark_of_completion = org_and_pedagogical_data[f'E{row}'].value
                Rich.debug_log(f"Отметка о выполнении: {mark_of_completion}")

                row_data = RowData(
                    work_name=name_of_work,
                    number_of_hours_for_work=number_of_hours,
                    period_of_execution_for_work=period_of_execution
                )

                list_of_types_of_jobs.append(row_data)

        organization_and_pedagogical_info = TeacherOrgAndPedagogicalInfo(
            total_hours=total_amount_of_planned_educational_and_methodological_work_for_academic_year,
            list_of_data_with_jobs=list_of_types_of_jobs
        )

        Rich.debug_log("Получена информация о организационной и воспитательной деятельности преподавателя")
        Rich.debug_log(f"Всего работ: {len(list_of_types_of_jobs)}")

        return organization_and_pedagogical_info

    @staticmethod
    def parse_professional_development_sheet(
            file_path: str) -> TeachersProfessionalDevelopmentInfo:
        """
        Функция для парсинга информации о повышении квалификации преподавателя.
        Информация парсится из листа 4 таблицы ИПРП

        :param file_path: путь к файлу таблицы ИПРП

        :return: TeachersProfessionalDevelopmentInfo - вернёт объект с данными
        """
        individual_plan = ParserITP.load_table(get_path_resources_file(file_path))
        # Открываю лист с работой по повышению квалификации - лист 4
        professional_development_data = individual_plan["4"]
        Rich.print_spacer()
        # Вывод шапки листа
        Rich.simple_log(" ".join((professional_development_data['A1'].value).split()))

        # Начало парсинга данных

        # Общий объём планируемой работы за учебный год, часов
        total_amount_of_planned_edu_and_method_work_for_academic_year = (
            float(professional_development_data['E3'].value)
        )
        Rich.debug_log(f"Общий объём планируемой работы за учебный год, часов: {
        total_amount_of_planned_edu_and_method_work_for_academic_year
        }")

        list_of_types_of_activities: List[RowDataProfessionalDevelopment] = []

        for row in range(7, professional_development_data.max_row - 1):
            if not professional_development_data[f'B{row}'].value is None:
                # Наименование мероприятия (включая наименование организации и
                # образовательной программы)
                name_of_activity = professional_development_data[f'B{row}'].value
                Rich.debug_log(f"Наименование мероприятия: {name_of_activity}")

                # Трудоёмкость, часов
                number_of_hours = float(professional_development_data[f'C{row}'].value)
                Rich.debug_log(f"Трудоёмкость, часов: {number_of_hours}")

                # Отметка о выполнении, реквизиты удостоверяющего документа
                mark_of_completion = professional_development_data[f'E{row}'].value
                Rich.debug_log(f"Отметка о выполнении, реквизиты удостоверяющего документа:"
                               f" {mark_of_completion}")

                row_data = RowDataProfessionalDevelopment(
                    activity_name=name_of_activity,
                    number_of_hours_for_work=number_of_hours,
                    mark_of_completion_activity=mark_of_completion
                )

                list_of_types_of_activities.append(row_data)

        professional_development_info = TeachersProfessionalDevelopmentInfo(
            total_hours=total_amount_of_planned_edu_and_method_work_for_academic_year,
            list_of_names_prof_dev_activities=list_of_types_of_activities
        )

        Rich.debug_log("Получена информация "
                       "о повышении квалификации преподавателя")
        if len(list_of_types_of_activities) == 0:
            Rich.warning_log("Информации о повышении квалификации преподавателя пуста")
        Rich.debug_log(f"Всего работ: {len(list_of_types_of_activities)}")

        return professional_development_info

    @staticmethod
    def parse_explanatory_notes_on_implementation_of_plan_sheet(file_path: str) -> List[str]:
        """
        Функция для парсинга листа 5 таблицы ИПРП
        :param file_path: путь к файлу таблицы ИПРП
        :return: List[str] - возвращает список с записями
        """
        individual_plan = ParserITP.load_table(get_path_resources_file(file_path))
        # Открываю лист 5
        explanatory_notes_data = individual_plan["5."]
        Rich.print_spacer()
        # Вывод шапки листа
        Rich.simple_log(" ".join((explanatory_notes_data['A1'].value).split()))

        list_of_data = []

        # парсинг данных
        for row in range(3, 45):
            if not explanatory_notes_data[f'A{row}'].value is None:
                data = explanatory_notes_data[f'A{row}'].value
                list_of_data.append(data)

        Rich.debug_log(f"Найдено записей: {len(list_of_data)}")

        if len(list_of_data) == 0:
            Rich.debug_log("Записей не найдено")

        Rich.success_log("Данные по изменениям, вносимым в ИПРП в процессе его "
                         "выполнения собраны")

        return list_of_data

    @staticmethod
    def parse_teachers_explanatory_notes_sheet(file_path: str) -> List[str]:
        """
        Функция для парсинга листа 6. таблицы ИПРП с данными по пояснительным
        запискам преподавателя

        :param file_path: путь к файлу таблицы ИПРП

        :return: List[str] - список записей с пояснительными записками преподавателя
        """
        individual_plan = ParserITP.load_table(get_path_resources_file(file_path))
        # Открываю лист 6.
        teachers_explanatory_notes_data = individual_plan["6."]
        Rich.print_spacer()
        # Вывод шапки листа
        Rich.simple_log(" ".join((teachers_explanatory_notes_data['A1'].value).split()))

        list_of_data = []

        # парсинг данных
        for row in range(3, 45):
            if not teachers_explanatory_notes_data[f'A{row}'].value is None:
                data = teachers_explanatory_notes_data[f'A{row}'].value
                list_of_data.append(data)

        Rich.debug_log(f"Найдено записей: {len(list_of_data)}")

        if len(list_of_data) == 0:
            Rich.debug_log("Записей не найдено")

        Rich.success_log("Данные по пояснительным запискам преподавателя собраны")

        return list_of_data

    @staticmethod
    def parse_application_additional_volume_sheet(
            file_path:str) -> TeachersAdditionalWorkData:
        """
        Функция для парсинга листа "Прил. 1 - Доп. объем" таблицы ИПРП.
        Парсит сведения об объёме нагрузки, выполняемых на условиях почасовой оплаты

        :param file_path: путь к файлу таблицы ИПРП

        :return: TeachersAdditionalWorkData возвращает объект датакласса
         с напарсенными данными
        """
        individual_plan = ParserITP.load_table(get_path_resources_file(file_path))
        # Открываю лист с учебной работой - лист "Прил. 1 - Доп. объем "
        additional_educational_work_data = individual_plan["Прил. 1 - Доп. объем"]
        Rich.print_spacer()
        # Вывод шапки листа
        Rich.simple_log(" ".join((additional_educational_work_data['A2'].value).split()))

        current_semester = ""
        current_group = ""

        list_of_disciplines_in_semester: List[InformationOnDisciplineOfAcademicWork] = []

        for row in range(8, additional_educational_work_data.max_row):
            # парсинг данных

            # парсинг по дисциплинам

            if not additional_educational_work_data[f'A{row}'].value is None:

                # Дальше парсинг данных по дисциплинам
                # название дисциплины
                subject_name = additional_educational_work_data[f'A{row}'].value
                Rich.debug_log(f"Дисциплина: {subject_name}")

                # Группа
                if not additional_educational_work_data[f'C{row}'].value is None:
                    current_group = additional_educational_work_data[f'C{row}'].value
                    Rich.debug_log(f"Группа: {current_group}")

                # Номер семестра (семестра обучения группы)
                educational_semester = additional_educational_work_data[f'D{row}'].value
                Rich.debug_log(f"Номер семестра: {educational_semester}")

                # Количество часов лекций
                hours_of_lectures = additional_educational_work_data[f'E{row}'].value
                if hours_of_lectures is None:
                    hours_of_lectures = 0
                hours_of_lectures = ParserITP.rounding(hours_of_lectures)
                Rich.debug_log(f"Часов лекций: {hours_of_lectures}")

                # Количество часов практики
                hours_of_practice_lessons = additional_educational_work_data[
                    f'F{row}'].value
                if hours_of_practice_lessons is None:
                    hours_of_practice_lessons = 0
                hours_of_practice_lessons = ParserITP.rounding(hours_of_practice_lessons)
                Rich.debug_log(f"Часов практики: {hours_of_practice_lessons}")

                # Количество часов лабораторных работ
                hours_of_laboratory_work = additional_educational_work_data[
                    f'G{row}'].value
                if hours_of_laboratory_work is None:
                    hours_of_laboratory_work = 0
                hours_of_laboratory_work = ParserITP.rounding(hours_of_laboratory_work)
                Rich.debug_log(f"Часов лабораторных работ: {hours_of_laboratory_work}")

                # Количество часов консультаций
                hours_of_consultations = additional_educational_work_data[
                    f'H{row}'].value
                if hours_of_consultations is None:
                    hours_of_consultations = 0
                hours_of_consultations = round(float(hours_of_consultations), 1)
                Rich.debug_log(f"Часов консультаций: {hours_of_consultations}")

                # Часов экзаменов
                hours_of_exams = additional_educational_work_data[
                    f'I{row}'].value
                if hours_of_exams is None:
                    hours_of_exams = 0
                hours_of_exams = round(float(hours_of_exams), 1)
                Rich.debug_log(f"Часов экзаменов: {hours_of_exams}")

                # Часов зачётов
                hours_of_credits = additional_educational_work_data[
                    f'J{row}'].value
                if hours_of_credits is None:
                    hours_of_credits = 0
                hours_of_credits = ParserITP.rounding(hours_of_credits)
                Rich.debug_log(f"Часов зачётов: {hours_of_credits}")

                # Часов курсовых работ, курсовых проектов
                hours_of_terms_works = additional_educational_work_data[
                    f'K{row}'].value
                if hours_of_terms_works is None:
                    hours_of_terms_works = 0
                hours_of_terms_works = ParserITP.rounding(hours_of_terms_works)
                Rich.debug_log(f"Часов курсовых работ, курсовых проектов: {hours_of_terms_works}")

                # Часов практики
                hours_of_practice = additional_educational_work_data[
                    f'L{row}'].value
                if hours_of_practice is None:
                    hours_of_practice = 0
                hours_of_practice = ParserITP.rounding(hours_of_practice)
                Rich.debug_log(f"Часов практики: {hours_of_practice}")

                # Часов ВКП
                hours_WRC = additional_educational_work_data[
                    f'M{row}'].value
                if hours_WRC is None:
                    hours_WRC = 0
                hours_WRC = ParserITP.rounding(hours_WRC)
                Rich.debug_log(f"Часов ВКР: {hours_WRC}")

                # Часов ГЭК
                hours_of_GEC = additional_educational_work_data[
                    f'N{row}'].value
                if hours_of_GEC is None:
                    hours_of_GEC = 0
                hours_of_GEC = ParserITP.rounding(hours_of_GEC)
                Rich.debug_log(f"Часов ГЭК: {hours_of_GEC}")

                # Часов дополнительных работ
                hours_of_additional_works = additional_educational_work_data[
                    f'O{row}'].value
                if hours_of_additional_works is None:
                    hours_of_additional_works = 0
                hours_of_additional_works = ParserITP.rounding(hours_of_additional_works)
                Rich.debug_log(f"Часов дополнительных работ: {hours_of_additional_works}")

                # Всего часов по плану
                hours_of_total_according_to_plan = additional_educational_work_data[
                    f'P{row}'].value
                if hours_of_total_according_to_plan is None:
                    hours_of_total_according_to_plan = 0
                hours_of_total_according_to_plan = round(float(hours_of_total_according_to_plan), 1)
                Rich.debug_log(f"Всего часов по плану: {hours_of_total_according_to_plan}")

                # Всего часов фактически
                hours_of_total_actually = additional_educational_work_data[
                    f'Q{row}'].value
                if hours_of_total_actually is None:
                    hours_of_total_actually = 0
                hours_of_total_actually = ParserITP.rounding(hours_of_total_actually)
                Rich.debug_log(f"Всего часов фактически: {hours_of_total_actually}")

                data_of_disciplines_in_semester = InformationOnDisciplineOfAcademicWork(
                    name_of_discipline=subject_name,
                    group=current_group,
                    number_of_semester=educational_semester,
                    lectures=hours_of_lectures,
                    practical_training=hours_of_practice_lessons,
                    laboratory_work=hours_of_laboratory_work,
                    consultations=hours_of_consultations,
                    exams=hours_of_exams,
                    credits=hours_of_credits,
                    term_papers_and_works=hours_of_terms_works,
                    practice=hours_of_practice,
                    WRC=hours_WRC,
                    GEK=hours_of_GEC,
                    additional_work=hours_of_additional_works,
                    total_according_plan=hours_of_total_according_to_plan,
                    total_actually=hours_of_total_actually
                )

                list_of_disciplines_in_semester.append(data_of_disciplines_in_semester)

        num_row_total_info_hours_educational_work_for_year = additional_educational_work_data.max_row - 1

        # Количество часов лекций - итог за год
        total_hours_of_lectures_by_year = additional_educational_work_data[
            f'E{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_of_lectures_by_year is None:
            total_hours_of_lectures_by_year = 0
        total_hours_of_lectures_by_year = round(float(total_hours_of_lectures_by_year),1)
        Rich.debug_log(f"Итоговое количество часов "
                       f"лекций за год: {total_hours_of_lectures_by_year}")

        # Количество часов практик - итог за год
        total_hours_of_practice_lessons_by_year = additional_educational_work_data[
            f'F{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_of_practice_lessons_by_year is None:
            total_hours_of_practice_lessons_by_year = 0
        total_hours_of_practice_lessons_by_year = round(float(total_hours_of_practice_lessons_by_year),1)
        Rich.debug_log(f"Итоговое количество часов "
                       f"практики за год: {total_hours_of_practice_lessons_by_year}")

        # Количество часов лабораторных работ - итог за год
        total_hours_of_laboratory_work_by_year = additional_educational_work_data[
            f'G{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_of_laboratory_work_by_year is None:
            total_hours_of_laboratory_work_by_year = 0
        total_hours_of_laboratory_work_by_year = round(float(total_hours_of_laboratory_work_by_year),1)
        Rich.debug_log(f"Итоговое количество часов "
                       f"лабораторных работ за год: {total_hours_of_laboratory_work_by_year}")

        # Количество часов консультаций - итог за год
        total_hours_of_consultations_by_year = additional_educational_work_data[
            f'H{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_of_consultations_by_year is None:
            total_hours_of_consultations_by_year = 0
        total_hours_of_consultations_by_year = round(float(total_hours_of_consultations_by_year),1)
        Rich.debug_log(f"Итоговое количество часов "
                       f"консультаций за год: {total_hours_of_consultations_by_year}")

        # Часов экзаменов - итог за год
        total_hours_of_exams_by_year = additional_educational_work_data[
            f'I{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_of_exams_by_year is None:
            total_hours_of_exams_by_year = 0
        total_hours_of_exams_by_year = round(float(total_hours_of_exams_by_year),1)
        Rich.debug_log(f"Итоговое количество часов "
                       f"экзаменов за год: {total_hours_of_exams_by_year}")

        # Часов зачётов - итог за год
        total_hours_of_credits_by_year = additional_educational_work_data[
            f'J{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_of_credits_by_year is None:
            total_hours_of_credits_by_year = 0
        total_hours_of_credits_by_year = round(float(total_hours_of_credits_by_year),1)
        Rich.debug_log(f"Итоговое количество часов "
                       f"зачётов за год: {total_hours_of_credits_by_year}")

        # Часов курсовых работ, курсовых проектов - итог за год
        total_hours_of_terms_works_by_year = additional_educational_work_data[
            f'K{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_of_terms_works_by_year is None:
            total_hours_of_terms_works_by_year = 0
        total_hours_of_terms_works_by_year = round(float(total_hours_of_terms_works_by_year),1)
        Rich.debug_log(f"Итоговое количество часов курсовых работ, курсовых "
                       f"проектов за год: {total_hours_of_terms_works_by_year}")

        # Часов практики - итог за год
        total_hours_of_practice_by_year = additional_educational_work_data[
            f'L{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_of_practice_by_year is None:
            total_hours_of_practice_by_year = 0
        total_hours_of_practice_by_year = round(float(total_hours_of_practice_by_year), 1)
        Rich.debug_log(f"Итоговое количество часов практики за год: "
                       f"{total_hours_of_practice_by_year}")

        # Часов ВКП - итог за год
        total_hours_WRC_by_year = additional_educational_work_data[
            f'M{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_WRC_by_year is None:
            total_hours_WRC_by_year = 0.0
        total_hours_WRC_by_year = round(float(total_hours_WRC_by_year),1)
        Rich.debug_log(f"Итоговое количество часов ВКР за год: {total_hours_WRC_by_year}")

        # Часов ГЭК - итог за год
        total_hours_of_GEC_by_year = additional_educational_work_data[
            f'N{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_of_GEC_by_year is None:
            total_hours_of_GEC_by_year = 0
        total_hours_of_GEC_by_year = round(float(total_hours_of_GEC_by_year),1)
        Rich.debug_log(f"Итоговое количество часов ГЭК за год: {total_hours_of_GEC_by_year}")

        # Часов дополнительных работ - итог за год
        total_hours_of_additional_works_by_year = additional_educational_work_data[
            f'O{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_of_additional_works_by_year is None:
            total_hours_of_additional_works_by_year = 0
        total_hours_of_additional_works_by_year = round(float(total_hours_of_additional_works_by_year),1)
        Rich.debug_log(f"Итоговое количество часов "
                       f"дополнительных работ за год: {total_hours_of_additional_works_by_year}")

        # Всего часов по плану - итог за год
        total_hours_of_total_according_to_plan_by_year = additional_educational_work_data[
            f'P{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_of_total_according_to_plan_by_year is None:
            total_hours_of_total_according_to_plan_by_year = 0
        total_hours_of_total_according_to_plan_by_year = round(float(total_hours_of_total_according_to_plan_by_year),1)
        Rich.debug_log(f"Итоговое количество часов "
                       f"по плану за год: {total_hours_of_total_according_to_plan_by_year}")

        # Всего часов фактически - итог за год
        total_hours_of_total_actually_by_year = additional_educational_work_data[
            f'Q{num_row_total_info_hours_educational_work_for_year}'].value
        if total_hours_of_total_actually_by_year is None:
            total_hours_of_total_actually_by_year = 0
        total_hours_of_total_actually_by_year = round(float(total_hours_of_total_actually_by_year), 1)
        Rich.debug_log(f"Итоговое количество "
                       f"часов фактически за год: {total_hours_of_total_actually_by_year}")

        summary_data_of_hours_teachers_additional_edu_work_by_year = SummaryInfoOnHoursOfTeachersAcademicWork(
            summary_lectures_per_year=total_hours_of_lectures_by_year,
            summary_practical_training_per_year=total_hours_of_practice_lessons_by_year,
            summary_laboratory_work_per_year=total_hours_of_laboratory_work_by_year,
            summary_consultations_per_year=total_hours_of_consultations_by_year,
            summary_exams_per_year=total_hours_of_exams_by_year,
            summary_credits_per_year=total_hours_of_credits_by_year,
            summary_term_papers_and_works_per_year=total_hours_of_terms_works_by_year,
            summary_practice_per_year=total_hours_of_practice_by_year,
            summary_WRC_per_year=total_hours_WRC_by_year,
            summary_GEK_per_year=total_hours_of_GEC_by_year,
            summary_additional_work_per_year=total_hours_of_additional_works_by_year,
            summary_total_according_plan_per_year=total_hours_of_total_according_to_plan_by_year,
            summary_total_actually=total_hours_of_total_actually_by_year
        )

        Rich.success_log("Сведения о дополнительном объёме нагрузки "
                             "преподавателя получены")
        Rich.debug_log(f"Записей: {len(list_of_disciplines_in_semester)}")

        teachers_educational_work = TeachersAdditionalWorkData(
            list_of_data_with_educational_work=list_of_disciplines_in_semester,
            summary_data_of_hours_additional_work=summary_data_of_hours_teachers_additional_edu_work_by_year
        )

        Rich.success_log("Добавлена информация о дополнительном объёме нагрузки преподавателя")
        ParserITP.list_with_data_of_teachers_additional_work.clear()

        return teachers_educational_work

    @staticmethod
    def parse_full_information(file_path: str) -> FullITP:
        """
        Функция для парсинга по всем листам таблицы ИПРП
        :param file_path: путь к файлу таблицы ИПРП
        :return: FullITP - возвращает объект с полными данными таблицы ИПРП
        """

        full_itp_info = FullITP(
            title_list_data = ParserITP.parse_title_sheet(file_path),
            general_data = ParserITP.parse_general_info_sheet(file_path),
            summary_data = ParserITP.parse_summary_data_sheet(file_path),
            education_work_data = ParserITP.parse_educational_work_sheet(file_path),
            educational_and_methodical_data = ParserITP.parse_educational_and_methodical_work_sheet(file_path),
            scientific_and_research_data  = ParserITP.parse_scientific_research_activities_sheet(file_path),
            organization_and_pedagogical_data = ParserITP.parse_organizational_and_pedagogical_activities_sheet(file_path),
            professional_development_data = ParserITP.parse_professional_development_sheet(file_path),
            explanatory_notes_on_implementation_of_plan_data = ParserITP.parse_explanatory_notes_on_implementation_of_plan_sheet(file_path),
            teachers_explanatory_notes_data = ParserITP.parse_teachers_explanatory_notes_sheet(file_path),
            application_additional_volume_data = ParserITP.parse_application_additional_volume_sheet(file_path)
        )

        return full_itp_info
