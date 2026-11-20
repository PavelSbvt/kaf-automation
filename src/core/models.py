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
