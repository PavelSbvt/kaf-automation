from dataclasses import dataclass
from typing import List


@dataclass
class TeacherGeneralInfo:
    """
    Датакласс для хранения сведений о преподавателе, которые указаны в таблице
    индивидуального плана преподавателя в листе общие сведения
    """
    # ФИО
    name: str
    # Должность
    post: str
    # Размер ставки
    amount_of_bet: float
    # Условия привлечения
    terms_of_attraction: str
    # Учёная степень
    academic_degree: str
    # Учёное звание
    academic_title: str
    # Сведения о контракте
    # information_about_contract: str
    # Дата, номер
    date_and_number: str
    # Срок действия
    validity_period: str
    # Базовое образование
    basic_education: str
    # Наименование образовательной программы
    name_educational_program: str
    # Квалификация
    qualification: str
    # Перечень преподаваемых дисциплин
    list_subjects_taught: List


@dataclass
class DataNamesOfWorksFromSummaryInfo:
    """
    Датакласс для хранения информации из строки с данными по видам работ преподавателя
    и указанным количеством часов.
    Данные берутся из листа "Сводные данные" таблицы ИПП
    """
    # наименование работы или вида деятельности
    activity_name: str
    # объём работы за указанный учебный год, часов
    amount_work_hours: float


@dataclass
class TeacherSummaryInfo:
    """
    Датакласс для хранения информации о сводных данных по видам работ преподавателя,
    которые парсятся из листа "Сводные данные по видам работ" из таблицы ИПП, по строкам
    с информацией
    """
    # данные в листе имеют подразделение только на два вида: наименование работ и
    # видов деятельности, поэтому буду хранить их в двух атрибутах

    # Шапка
    name_of_work_and_types_of_activity = "Наименование работ и видов деятельности"

    # Информация из ячейки объёма работы за указанный год
    # (для того, чтобы иметь данные о годе)
    year_is_amount_of_work_indicated: str

    # Список с данными по наименованиям работ и видам деятельности
    list_data_of_names_of_works: List[DataNamesOfWorksFromSummaryInfo]

    # Итоговая информация по общему количеству часов
    total_hours: float
