"""Файл с классом-парсером для 'САПР отчёт' на openpyxl"""

from typing import List

from parser.sapr_report_models import (
    TitleInfo,
    MemberOfDepartment)
from utils.output_rich import Rich
from utils.utils_funcs import rounding, load_table, get_path_resources_file


class ParserReportSAPR:
    """
    Класс-обёртка для методов парсеров для документа 'Отчёт САПР'
    """

    @staticmethod
    def parse_title_sheet(file_path: str) -> TitleInfo:
        """
        Метод для парсинга титульного листа отчёта САПР

        :param file_path: путь к документу

        :return: TitleInfo - информация из титульного листа
        """
        individual_plan = load_table(get_path_resources_file(file_path))
        # Открываю титульный лист
        tit_list_info = individual_plan["Титульный лист"]
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
        individual_plan = load_table(get_path_resources_file(file_path))
        # Открываю лист кадрового состава кафедры
        composition_info = individual_plan["Состав кафедры"]
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
