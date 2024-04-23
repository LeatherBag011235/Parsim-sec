import os
import polars as pl
import numpy as np 


def make_texts_same_len(company_dict): 

    max_length = max(len(lst) for lst in company_dict.values())

    for key in company_dict:
        additional_length = max_length - len(company_dict[key])
        company_dict[key] = company_dict[key] + [np.nan] * additional_length

    return company_dict


def extract_strings():

    base_directory = 'cleared_strings'

    # Dictionary to hold processed data for each company
    dict_with_all_companies = {}

    # Traverse each subdirectory in the base directory
    for company_dir in os.listdir(base_directory):
       
        company_path = os.path.join(base_directory, company_dir)

        if os.path.isdir(company_path):

            company_dict = {} 
            
            for filename in os.listdir(company_path):
                
                file_path = os.path.join(company_path, filename)

                with open(file_path, 'r') as file:

                    data = file.read()
                    company_dict[filename] = data.split()

            dict_with_all_companies[company_dir] = make_texts_same_len(company_dict)
    
    return dict_with_all_companies

            

def save_to_parquet(company_name, company_dict):

    df = pl.DataFrame(company_dict)

    # Determine the output directory and file name
    output_dir = os.path.join('.', 'polars_dfs')
    os.makedirs(output_dir, exist_ok=True)

    file_name_new = f"{company_name}_reports.parquet"
    full_path = os.path.join(output_dir, file_name_new)
    full_path = os.path.normpath(full_path)

    print(f"Attempting to write to: {full_path}")

    # Write the DataFrame to Parquet
    df.write_parquet(full_path)

    print(f"{full_path} created successfully")
                    
            

