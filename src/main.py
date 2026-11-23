from core.data_keeper import (
    save_itp_general_data,
    save_itp_summary_data,
    save_itp_educational_work_data,
    save_itp_educational_and_methodical_work_data,
    save_itp_scientific_and_research_data,
    save_itp_organization_and_pedagogical_data,
    save_itp_professional_development_data,
    save_full_itp_data)
from parser.itp_parser import ParserITP


def main():

    save_full_itp_data("tables/itp/individ_plrpr2023 Обухов.xlsx")


if __name__ == "__main__":
    main()
