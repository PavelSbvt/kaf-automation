"""Файл с моделями данных для класса-парсера отчёта САПРа"""

from typing import List
from dataclasses import dataclass


@dataclass
class TitleInfo:
    """
    Датакласс для хранения информации с титульного листа отчёта САПРа
    """
    report_by_year: str
    """отчёт о выполнении учебной работы за такой то учебный год"""

    institute: str
    """Институт"""

    name_of_department: str
    """Наименование кафедры"""

    # Информация о зав кафедрой
    academic_degree: str
    """учёная степень"""

    academic_title: str
    """Учёное звание"""

    name_of_head_of_department: str
    """ФИО заведующей кафедрой"""


@dataclass
class MemberOfDepartment:
    """
    Датакласс для хранения информации по члену кафедры из листа Состав кафедры отчёта САПРа
    """
    members_fio: str
    """ФИО преподавателя"""

    terms_to_attraction: str
    """условия привлечения"""

    post: str
    """Должность"""

    academical_degree: str
    """Учёная степень"""

    academical_title: str
    """Учёное звание"""
