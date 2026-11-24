"""Файл с классом-парсером для 'САПР отчёт' на openpyxl"""

from typing import List

from parser.sapr_report_models import (
    TitleInfo,
    MemberOfDepartment,
    ReportInfo,
    FullInfoOfReport)
from utils.output_rich import Rich
from utils.utils_funcs import rounding, load_table, get_path_resources_file


class ParserReportSAPR:
    """
    Класс-обёртка для методов парсеров на openpyxl для документа 'Отчёт САПР'

    Парсит листы:
    - Титульный лист
    - Состав кафедры
    - Отчёт

    Содержит статические методы для парсинга отдельных листов таблицы
    """

    @staticmethod
    def parse_title_sheet(file_path: str) -> TitleInfo:
        """
        Метод для парсинга титульного листа отчёта САПР

        :param file_path: путь к документу

        :return: TitleInfo - информация из титульного листа
        """
        sapr_report = load_table(get_path_resources_file(file_path))
        # Открываю титульный лист
        tit_list_info = sapr_report["Титульный лист"]
        Rich.simple_log(f"{tit_list_info['A4'].value}")
        Rich.print_spacer()

        # Парсинг
        # за учебный год
        year_of_report = tit_list_info['A6'].value
        Rich.debug_log(f"Отчёт о выполнении учебной работы {year_of_report}")

        # институт
        institute_info = tit_list_info['A8'].value
        Rich.debug_log(f"Институт: {institute_info}")

        # Наименование кафедры
        departments_name = tit_list_info['A11'].value
        Rich.debug_log(f"Кафедра: {departments_name}")

        # учёная степень зав кафедрой
        academic_degree = tit_list_info['H21'].value
        Rich.debug_log(f"Учёная степень зав кафедрой: {academic_degree}")

        # учёное звание зав кафедрой
        academic_title = tit_list_info['H23'].value
        Rich.debug_log(f"Учёное звание зав кафедрой: {academic_title}")

        # ФИО зав кафедрой
        fio_head = tit_list_info['H25'].value
        Rich.debug_log(f"ФИО зав кафедрой: {fio_head}")

        title_sheet_data = TitleInfo(
            report_by_year = year_of_report,
            institute = institute_info,
            name_of_department = departments_name,
            academic_degree = academic_degree,
            academic_title = academic_title,
            name_of_head_of_department = fio_head
        )

        Rich.success_log("Получена информация из титульного листа")
        return title_sheet_data

    @staticmethod
    def parse_composition_of_department_sheet(file_path: str) -> List[MemberOfDepartment]:
        """
        Функция для сбора данных о составе кафедры
        :param file_path: путь к файлу отчёта
        :return: список с объектами MemberOfDepartment с полной информацией по
         каждому члену состава кафедры
        """
        sapr_report = load_table(get_path_resources_file(file_path))
        # Открываю лист кадрового состава кафедры
        composition_info = sapr_report["Состав кафедры"]
        title = composition_info['A1'].value + composition_info['A2'].value
        Rich.simple_log(f"{title}")
        Rich.print_spacer()

        list_of_members: List[MemberOfDepartment] = []

        # парсинг данных
        for row in range(6, 200):
            if not composition_info[f'B{row}'].value is None:
                # ФИО преподавателя
                fio = composition_info[f'B{row}'].value
                Rich.debug_log(f"Преподаватель: {fio}")

                # условия привлечения
                term_to_attraction = composition_info[f'C{row}'].value
                Rich.debug_log(f"Условия привлечения: {term_to_attraction}")

                # Должность
                member_post = composition_info[f'D{row}'].value
                Rich.debug_log(f"Должность: {member_post}")

                # Учёная степень
                academic_degree = composition_info[f'E{row}'].value
                Rich.debug_log(f"Учёная степень: {academic_degree}")

                # Учёное звание
                academic_title = composition_info[f'F{row}'].value
                Rich.debug_log(f"Учёное звание: {academic_title}")

                Rich.print_spacer_points()

                member_info = MemberOfDepartment(
                    members_fio = fio,
                    terms_to_attraction = term_to_attraction,
                    post = member_post,
                    academical_degree = academic_degree,
                    academical_title = academic_title
                )

                list_of_members.append(member_info)

        Rich.success_log("Получена информация по составу кафедры")
        Rich.debug_log(f"Найдено членов: {len(list_of_members)}")

        return list_of_members

    @staticmethod
    def parse_report_sheet(file_path: str) -> ReportInfo:
        """
        Метод для парсинга листа Отчёт таблицы Отчёт САПР
        :param file_path: путь к файлу отчёта
        :return: ReportInfo - объект с данными листа отчёта
        """
        sapr_report = load_table(get_path_resources_file(file_path))
        # Открываю лист кадрового состава кафедры
        report_info = sapr_report["Отчет"]
        Rich.simple_log(f"Отчёт о выполнении учебной работы "
                        f"{report_info['A3'].value}")
        Rich.print_spacer()

        # данные
        # учебный год
        report_year = report_info['A3'].value
        Rich.debug_log(f"Отчёт {report_year}")

        # фактический общий объём учебной нагрузки
        fact_educational_load = report_info['E8'].value
        fact_educational_load = rounding(fact_educational_load)
        Rich.debug_log(f"фактический общий объём учебной нагрузки: "
                       f"{fact_educational_load}")

        # объяснение причин отклонения
        explanation_of_reasons_for_rejection = report_info['A11'].value
        if explanation_of_reasons_for_rejection is None:
            explanation_of_reasons_for_rejection = "Не указано"
        Rich.debug_log(f"Объяснение причин отклонения: "
                       f"{explanation_of_reasons_for_rejection}")

        Rich.simple_log(report_info['A13'].value)
        Rich.print_spacer()

        # данные по разбиениям нагрузки на часы
        # Лекции
        hours_of_lectures = float(report_info['A18'].value)
        hours_of_lectures = rounding(hours_of_lectures)
        Rich.debug_log(f"Часов лекций: {hours_of_lectures}")

        # Практические занятия
        hours_of_practical_lessons = report_info['B18'].value
        hours_of_practical_lessons = rounding(hours_of_practical_lessons)
        Rich.debug_log(f"Часов практических занятий: {hours_of_practical_lessons}")

        # лабораторные работы
        hours_of_laboratory_lessons = report_info['C18'].value
        hours_of_laboratory_lessons = rounding(hours_of_laboratory_lessons)
        Rich.debug_log(f"Часов лабораторных работ: {hours_of_laboratory_lessons}")

        # консультации
        hours_of_consultations = report_info['D18'].value
        hours_of_consultations = rounding(hours_of_consultations)
        Rich.debug_log(f"Часов консультаций: {hours_of_consultations}")

        # экзамены
        hours_of_exams = report_info['E18'].value
        hours_of_exams = rounding(hours_of_exams)
        Rich.debug_log(f"Часов экзаменов: {hours_of_exams}")

        # зачёты
        hours_of_credits = report_info['F18'].value
        hours_of_credits = rounding(hours_of_credits)
        Rich.debug_log(f"Часов зачётов: {hours_of_credits}")

        # курсовые работы, курсовые проекты
        hours_of_terms_works = report_info['G18'].value
        hours_of_terms_works = rounding(hours_of_terms_works)
        Rich.debug_log(f"Часов курсовых работ и проектов: {hours_of_terms_works}")

        # практика
        hours_of_practice = report_info['H18'].value
        hours_of_practice = rounding(hours_of_practice)
        Rich.debug_log(f"Часов практик: {hours_of_practice}")

        # ВКР
        hours_of_WKP = report_info['I18'].value
        hours_of_WKP = rounding(hours_of_WKP)
        Rich.debug_log(f"Часов ВКП: {hours_of_WKP}")

        # ГЭК
        hours_of_GEC = report_info['J18'].value
        hours_of_GEC = rounding(hours_of_GEC)
        Rich.debug_log(f"Часов ГЭК: {hours_of_GEC}")

        # Дополнительная работа
        hours_of_additional_work = report_info['K18'].value
        hours_of_additional_work = rounding(hours_of_additional_work)
        Rich.debug_log(f"Часов дополнительной работы: {hours_of_additional_work}")

        # Итого
        summary_hours = report_info['L18'].value
        summary_hours = rounding(summary_hours)
        Rich.debug_log(f"Итого часов: {summary_hours}")

        # Из столбца 12 дополнительный объем нагрузки, в том числе выполненной
        # на условиях почасовой оплаты
        hours_of_additional_load = report_info['M18'].value
        hours_of_additional_load = rounding(hours_of_additional_load)
        Rich.debug_log("Часов дополнительной нагрузки из столбца 12: "
                       f"{hours_of_additional_load}")

        info_fact_working_volume = ReportInfo(
            year_of_report = report_year,
            hours_of_fact_educational_load = fact_educational_load,
            explanation_of_reasons_for_rejection_info = explanation_of_reasons_for_rejection,
            hours_lectures = hours_of_lectures,
            practical_training = hours_of_practical_lessons,
            hours_laboratory_work = hours_of_laboratory_lessons,
            hours_consultations = hours_of_consultations,
            hours_exams = hours_of_exams,
            hours_credits = hours_of_credits,
            term_papers_and_works = hours_of_terms_works,
            practice = hours_of_practice,
            WRC = hours_of_WKP,
            GEK = hours_of_GEC,
            additional_work = hours_of_additional_work,
            total_according = summary_hours,
            hours_by_12_column = hours_of_additional_work
        )

        Rich.success_log("Получена информация по отчёту")
        return info_fact_working_volume

    @staticmethod
    def parse_full_info(file_path: str) -> FullInfoOfReport:
        """
        Функция для парсинга всех листов отчёта САПРа
        :param file_path: путь к файлу таблицы отчёта САПРа
        :return: FullInfoOfReport - объект с полной информацией по документу
        """

        title_sheet_info = ParserReportSAPR.parse_title_sheet(file_path)

        department_structure_sheet_info = (
            ParserReportSAPR.parse_composition_of_department_sheet(file_path))

        report_sheet_info = ParserReportSAPR.parse_report_sheet(file_path)

        full_parsed_info = FullInfoOfReport(
            title_info = title_sheet_info,
            department_structure = department_structure_sheet_info,
            report_info = report_sheet_info
        )

        Rich.debug_log("Получены данные парсинга Отчёта САПРа")
        return full_parsed_info
