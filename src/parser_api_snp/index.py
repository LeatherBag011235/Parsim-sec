from .utils import *


#####################################################
years = [2019, 2020, 2021, 2022, 2023]
qtrs = [1, 2, 3, 4]
#####################################################

def get_company_links_object():
    all_lines = []

    for year in years:
        for qrt in qtrs:

            lines = download_report(year, qrt)
            
            all_lines.extend(lines)
            print(year, qrt)


    reports_df = get_all_links(all_lines)

    snp_quarter_df = get_snp_links(reports_df)

    company_links_object = compile_links(snp_quarter_df)
    
    return company_links_object


