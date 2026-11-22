# from pathlib import Path

from core.data_keeper import (
    save_itp_general_data,
    save_itp_summary_data,
    save_itp_educational_work_data,
    save_itp_educational_and_methodical_work_data,
    save_itp_scientific_and_research_data,
    save_itp_organization_and_pedagogical_data,
    save_itp_professional_development_data)
from parser.itp_parser import ParserITP


def main():
    # ParserITP.parse_professional_development_sheet("tables/itp/individ_plrpr2024 Волков.xlsx")
    # save_itp_professional_development_data(ParserITP.ITP_TEACHERS_PROFESSIONAL_DEVELOPMENT_DATA)

    ParserITP.parse_title_sheet("tables/itp/individ_plrpr2024 Волков.xlsx")


if __name__ == "__main__":
    main()
