from dataclasses import dataclass
from typing import List


@dataclass
class InfoFromTitlePage:
    """
    Датакласс для хранения основной информации с титульного листа ИПРП преподавателя
    """
    year_doc_created: str
    """Год составления документа"""

    date_of_meeting: str
    """Рассмотрено на заседании - дата рассмотрения"""

    number_of_protocol_of_meeting: str
    """Номер протокола заседания"""

    who_approved: str
    """Кем утверждён ИПРП"""

    date_of_approved: str
    """Дата утверждения ИПРП"""

    department: str
    """Кафедра"""

    institute: str
    """Институт"""

    teachers_fio: str
    """Фамилия, имя и отчество преподавателя"""

    name_of_position: str
    """Наименование должности"""

    year_of_plan: str
    """На какой учебный год составлен ИПРП"""


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

    summary_data_of_hours_by_semester: TeachersSummaryInfoOnHoursOfWorkPerSemester
    """Список с итоговой информацией по часам работы преподавателя в семестре"""


@dataclass
class SummaryInfoOnHoursOfTeachersAcademicWork:
    """
    Итоговая информация по часам работы учебной работы преподавателя за год.
    Берётся из листа 1.1 таблицы ИПП
    """
    summary_lectures_per_year: float
    """Лекции - итоговое количество часов за год"""

    summary_practical_training_per_year: float
    """Практические занятия - итоговое количество часов за год"""

    summary_laboratory_work_per_year: float
    """Лабораторные работы - итоговое количество часов за год"""

    summary_consultations_per_year: float
    """Консультации - итоговое количество часов за год"""

    summary_exams_per_year: float
    """Экзамены - итоговое количество часов за год"""

    summary_credits_per_year: float
    """Зачёты - итоговое количество часов за год"""

    summary_term_papers_and_works_per_year: float
    """Курсовые работы, курсовые проекты - итоговое количество часов за год"""

    summary_practice_per_year: float
    """Практика - итоговое количество часов за год"""

    summary_WRC_per_year: float
    """ВКР - итоговое количество часов за год"""

    summary_GEK_per_year: float
    """ГЭК - итоговое количество часов за год"""

    summary_additional_work_per_year: float
    """Дополнительные работы - итоговое количество часов за год"""

    summary_total_according_plan_per_year: float
    """Всего по плану - итоговое количество часов за год"""

    summary_total_actually: float
    """Фактически выполнено за семестр - итоговое количество часов за год"""


@ dataclass
class FullInfoOnEducationWorkOfTeacher:
    """
    Датакласс для хранения полной информации по учебному плану преподавателя.
    Данные из листа 1.1 таблицы ИПП.
    """
    autumn_semester: TeacherAcademicWorkPerSemester
    """Информация по осеннему семестру"""

    spring_semester: TeacherAcademicWorkPerSemester
    """Информация по весеннему семестру"""

    summary_info_about_educational_work_by_year: SummaryInfoOnHoursOfTeachersAcademicWork | None
    """Итоговая информация по часам учебной работы"""


@dataclass
class RowData:
    """
    Датакласс для хранения данных строки таблицы (наименование работы, трудоёмкость в
     часах, срок выполнения) для листов таблицы ИПП
    """
    work_name: str
    """Наименование вида работы"""

    number_of_hours_for_work: float
    """Трудоёмкость, часов"""

    period_of_execution_for_work: str
    """Срок выполнения (месяц, год)"""


@dataclass
class TeacherEducationalAndMethodicalWorkData:
    """
    Датакласс для хранения информации об учебно-методической работе преподавателя.
    Хранит информацию с листа 1.2 таблицы ИПП
    """
    total_hours: float
    """Общий объем планируемой учебно-методической работы за учебный год, часов"""

    list_of_data_with_jobs: List[RowData]
    """Список с видами работ, трудоёмкостью в часах и сроках выполнения"""


@dataclass
class TeacherScientificAndResearchInfo:
    """
    Датакласс для хранения информации о научно-исследовательской деятельности
     преподавателя. Для хранения данных листа 2 таблицы ИПП
    """
    total_hours: float
    """Общий объем планируемой научно-исследовательской деятельности за учебный год, 
    часов"""

    list_of_data_with_jobs: List[RowData]
    """Список с видами работ, трудоёмкостью в часах и сроках выполнения"""


@dataclass
class TeacherOrgAndPedagogicalInfo:
    """
    Датакласс для хранения информации об организационной и воспитательной деятельности
     преподавателя. Для хранения данных листа 3 таблицы ИПП
    """
    total_hours: float
    """Общий объем планируемой организационной и воспитательной деятельности 
    за учебный год, часов"""

    list_of_data_with_jobs: List[RowData]
    """Список с видами работ, трудоёмкостью в часах и сроках выполнения"""


@dataclass
class RowDataProfessionalDevelopment:
    """
    Датакласс для хранений информации из строки таблицы с листа 4 ИПП - строки с
     данными о повышении квалификации преподавателя
    """
    activity_name: str
    """Наименование мероприятия 
    (включая наименование организации и образовательной программы)"""

    number_of_hours_for_work: float
    """Трудоёмкость часов"""

    mark_of_completion_activity: str
    """Отметка о выполнении, реквизиты удостоверяющего документа"""


@dataclass
class TeachersProfessionalDevelopmentInfo:
    """Датакласс для хранения информации из листа повышения квалификации преподавателя
     - лист 4 таблицы ИПП
     """
    total_hours: float
    """Общий объем планируемых работ по повышению квалификации 
    за учебный год, часов"""

    list_of_names_prof_dev_activities: List[RowDataProfessionalDevelopment]
    """
    Массив с данными по наименованию мероприятия, его трудоёмкости в часах и 
    отметки о выполнении с реквизитами удостоверяющего документа
    """