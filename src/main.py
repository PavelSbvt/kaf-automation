# from pathlib import Path

from core.data_keeper import (
    save_itp_general_data,
    save_itp_summary_data,
    save_itp_educational_work_data,
    save_itp_educational_and_methodical_work_data,
    save_itp_scientific_and_research_data)
from parser.itp_parser import (
    parse_general_info_sheet,
    ITP_TEACHERS_GENERAL_DATA,
    parse_summary_data_sheet,
    ITP_TEACHERS_SUMMARY_DATA,
    parse_educational_work_sheet,
    ITP_TEACHERS_EDUCATIONAL_DATA,
    parse_educational_and_methodical_work_sheet,
    ITP_TEACHERS_EDUCATIONAL_AND_METHODICAL_DATA,
    parse_scientific_research_activities_sheet,
    ITP_TEACHERS_SCIENTIFIC_AND_RESEARCH_DATA)


def main():
    # parse_general_info_sheet("tables/itp/individ_plrpr2023 Волков.xlsx")
    # parse_general_info_sheet("tables/itp/individ_plrpr2023 Обухов.xlsx")
    # parse_general_info_sheet("tables/itp/individ_plrpr2023 Патутин.xlsx")
    # parse_general_info_sheet("tables/itp/individ_plrpr2023 Свешников.xlsx")
    # parse_general_info_sheet("tables/itp/individ_plrpr2024 Волков.xlsx")
    # parse_general_info_sheet("tables/itp/individ_plrpr2024 Свешников.xlsx")
    # parse_general_info_sheet("tables/itp/individ_plrpr2025 Волков.xlsx")
    # parse_general_info_sheet("tables/itp/individ_plrpr2025 Свешников.xlsx")
    # parse_general_info_sheet("tables/itp/!!! individ_plrpr2025 Архипов.xlsx")
    #
    # save_itp_general_data(ITP_TEACHERS_GENERAL_DATA)

    # parse_summary_data("tables/itp/individ_plrpr2023 Волков.xlsx")
    # parse_summary_data("tables/itp/individ_plrpr2023 Обухов.xlsx")
    # parse_summary_data("tables/itp/individ_plrpr2023 Патутин.xlsx")
    # parse_summary_data("tables/itp/individ_plrpr2023 Свешников.xlsx")
    # parse_summary_data("tables/itp/individ_plrpr2024 Волков.xlsx")
    # parse_summary_data("tables/itp/individ_plrpr2024 Свешников.xlsx")
    # parse_summary_data("tables/itp/individ_plrpr2025 Волков.xlsx")
    # parse_summary_data("tables/itp/individ_plrpr2025 Свешников.xlsx")
    # parse_summary_data("tables/itp/!!! individ_plrpr2025 Архипов.xlsx")
    #
    # save_itp_summary_data(ITP_TEACHERS_SUMMARY_DATA)

    # parse_educational_work_sheet("tables/itp/individ_plrpr2023 Волков.xlsx")
    # save_itp_educational_work_data(ITP_TEACHERS_EDUCATIONAL_DATA)

    # parse_educational_and_methodical_work_sheet("tables/itp/individ_plrpr2024 Волков.xlsx")
    # save_itp_educational_and_methodical_work_data(ITP_TEACHERS_EDUCATIONAL_AND_METHODICAL_DATA)

    parse_scientific_research_activities_sheet("tables/itp/individ_plrpr2024 Волков.xlsx")
    save_itp_scientific_and_research_data(ITP_TEACHERS_SCIENTIFIC_AND_RESEARCH_DATA)


if __name__ == "__main__":
    main()
