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


@dataclass
class InformationOnDisciplineOfAcademicWork:
    """
    Датакласс для хранения информации по дисциплине из учебной работы преподавателя.
    Информация из листа 1.1 таблицы ИПП
    """
    # Наименование дисциплины
    name_of_discipline: str
    # Группа
    group: str
    # Номер семестра
    number_of_semester: int
    # Лекции
    lectures: float
    # Практические занятия
    practical_training: float
    # Лабораторные работы
    laboratory_work: float
    # Консультации
    consultations: float
    # Экзамены
    exams: float
    # Зачёты
    credits: float
    # Курсовые работы, курсовые проекты
    term_papers_and_works: float
    # Практика
    practice: float
    # ВКР
    WRC: float
    # ГЭК
    GEK: float
    # Дополнительные работы
    additional_work: float
    # Всего по плану
    total_according_plan: float
    # Фактически выполнено за семестр
    total_actually: float


@dataclass
class TeachersSummaryInfoOnHoursOfWorkPerSemester:
    """
    Датакласс для хранения информации по итоговому количеству часов по
     учебной работе преподавателя в семестре их листа 1.1. таблицы ИПП
    """

    summary_lectures: float
    """Лекции - итоговое количество часов за семестр"""

    summary_practical_training: float
    """Практические занятия - итоговое количество часов за семестр"""

    summary_laboratory_work: float
    """Лабораторные работы - итоговое количество часов за семестр"""

    summary_consultations: float
    """Консультации - итоговое количество часов за семестр"""

    summary_exams: float
    """Экзамены - итоговое количество часов за семестр"""

    summary_credits: float
    """Зачёты - итоговое количество часов за семестр"""

    summary_term_papers_and_works: float
    """Курсовые работы, курсовые проекты - итоговое количество часов за семестр"""

    summary_practice: float
    """Практика - итоговое количество часов за семестр"""

    summary_WRC: float
    """ВКР - итоговое количество часов за семестр"""

    summary_GEK: float
    """ГЭК - итоговое количество часов за семестр"""

    summary_additional_work: float
    """Дополнительные работы - итоговое количество часов за семестр"""

    summary_total_according_plan: float
    """Всего по плану - итоговое количество часов за семестр"""

    summary_total_actually: float
    """Фактически выполнено за семестр - итоговое количество часов за семестр"""


@dataclass
class TeacherAcademicWorkPerSemester:
    """
    Датакласс для хранения данных по учебной работы преподавателя по одному семестру
    (осеннему или весеннему).
    Данные из листа "1.1. " ИПП.
    """

    semester: str
    """Семестр"""

    disciplines: List[InformationOnDisciplineOfAcademicWork]
    """Список дисциплин с информацией по каждой"""

    summary_data_of_hours: TeachersSummaryInfoOnHoursOfWorkPerSemester
    """Список с итоговой информацией по часам работы преподавателя в семестре"""

