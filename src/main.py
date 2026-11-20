# from pathlib import Path

from parser.itp_parser import parse_general_info_sheet


def main():
    parse_general_info_sheet("tables/itp/individ_plrpr2023 Волков.xlsx")

if __name__ == "__main__":
    main()
