from .utils import *

def convert_files():
    dict_with_all_companies = extract_strings()

    for company_name, company_dict in dict_with_all_companies.items():
        print(company_name)
        save_to_parquet(company_name, company_dict)