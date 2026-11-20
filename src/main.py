# from pathlib import Path

from core.data_keeper import save_itp_data
from parser.itp_parser import parse_general_info_sheet, ITP_TEACHERS_DATA


def main():
    parse_general_info_sheet("tables/itp/individ_plrpr2023 Волков.xlsx")
    parse_general_info_sheet("tables/itp/individ_plrpr2023 Обухов.xlsx")
    parse_general_info_sheet("tables/itp/individ_plrpr2023 Патутин.xlsx")
    parse_general_info_sheet("tables/itp/individ_plrpr2023 Свешников.xlsx")
    parse_general_info_sheet("tables/itp/individ_plrpr2024 Волков.xlsx")
    parse_general_info_sheet("tables/itp/individ_plrpr2024 Свешников.xlsx")
    parse_general_info_sheet("tables/itp/individ_plrpr2025 Волков.xlsx")
    parse_general_info_sheet("tables/itp/individ_plrpr2025 Свешников.xlsx")
    parse_general_info_sheet("tables/itp/!!! individ_plrpr2025 Архипов.xlsx")

    save_itp_data(ITP_TEACHERS_DATA)


if __name__ == "__main__":
    main()
