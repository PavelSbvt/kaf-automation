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


@dataclass
class ReportInfo:
    """
    Класс для хранения данных листа Отчёт таблицы Отчёт САПР.
    """
    year_of_report: str
    """За какой год отчёт"""

    hours_of_fact_educational_load: float
    """Часов фактического общего объёма работы на кафедре"""

    explanation_of_reasons_for_rejection_info: str
    """Объяснение причин отклонений"""

    hours_lectures: float
    """Часов лекции"""

    practical_training: float
    """Часов практические занятия"""

    hours_laboratory_work: float
    """Часов лабораторные работы"""

    hours_consultations: float
    """Часов консультации"""

    hours_exams: float
    """Часов экзамены"""

    hours_credits: float
    """Часов эачётов"""

    term_papers_and_works: float
    """Курсовые работы, курсовые проекты"""

    practice: float
    """Практика"""

    WRC: float
    """ВКР"""

    GEK: float
    """ГЭК"""

    additional_work: float
    """Дополнительные работы"""

    total_according: float
    """Итого часов фактического объёма нагрузки"""

    hours_by_12_column: float
    """
    Из столбца 12 дополнительный объем нагрузки, в том числе выполненной 
    на условиях почасовой оплаты
    """


@dataclass
class FullInfoOfReport:
    """
    Датакласс для хранения полной информации по отчёту САПРа
    """
    title_info: TitleInfo
    """Информация с титульного листа"""

    department_structure: List[MemberOfDepartment]
    """Список с составом кафедры (элемент списка - преподаватель)"""

    report_info: ReportInfo
    """Информация из листа отчёта"""
