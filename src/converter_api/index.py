from .utils import *

def convert_files(files_to_convert):

    output_dir_for_get, output_dir_for_save = spesify_dir(files_to_convert)
    print('dirs have been specified')

    dict_with_all_companies = extract_strings(output_dir_for_get)
    print("strings have been extracted")

    for company_name, company_dict in dict_with_all_companies.items():
        print(company_name)
        save_to_parquet(company_name, company_dict, output_dir_for_save)