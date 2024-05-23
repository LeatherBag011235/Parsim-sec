import os
import numpy as np 
import re
import polars as pl


def spesify_dir(files_to_convert):
    #spesify directory to get files for converting
    output_dir_for_get = os.path.join('raw_data', files_to_convert)

    res_dir = f'{files_to_convert}_upd'

    #spesify directory to save converted files 
    output_dir_for_save = os.path.join('prepared_data', res_dir)

    return output_dir_for_get, output_dir_for_save




def make_texts_same_len(company_dict): 

    max_length = max(len(lst) for lst in company_dict.values())

    for key in company_dict:
        additional_length = max_length - len(company_dict[key])
        company_dict[key] = company_dict[key] + [np.nan] * additional_length

    return company_dict


def set_of_sentimen_words():
    lm_dict = pl.read_csv(r'C:\Users\310\Desktop\Progects_Py\Parsim-sec\src\converter_api\Loughran-McDonald_MasterDictionary_1993-2021.csv')
    hv_dict = pl.read_excel(r'C:\Users\310\Desktop\Progects_Py\Parsim-sec\src\converter_api\Harvard_inquirerbasic.xls')

    positive_words_lm = lm_dict.filter(lm_dict["Positive"] > 0)
    negative_words_lm = lm_dict.filter(lm_dict["Negative"] > 0)

    lm_words = positive_words_lm.vstack(negative_words_lm)
    lm_words = lm_words.to_series().str.to_lowercase()
    lm_words = lm_words.to_frame('column_0')

    positive_words_hv = hv_dict.filter(hv_dict["Positiv"] == 'Positiv')
    negative_words_hv = hv_dict.filter(hv_dict["Negativ"] == 'Negativ')

    hv_words = positive_words_hv.vstack(negative_words_hv)
    hv_words = hv_words.to_series().str.to_lowercase()
    hv_words = hv_words.map_elements(lambda word: re.sub(r'#\d+', '', word))
    hv_words = hv_words.to_frame('column_0')
    
    all_needed_words = lm_words.vstack(hv_words).drop_nulls()

    return all_needed_words.unique()




def extract_strings(base_directory):

    sentiment_words = set_of_sentimen_words()

    date_pattern = re.compile(r'(\d{4}-\d{2}-\d{2})')

    # Dictionary to hold processed data for each company
    dict_with_all_companies = {}

    # Traverse each subdirectory in the base directory
    for company_dir in os.listdir(base_directory):
       
        company_path = os.path.join(base_directory, company_dir)

        if os.path.isdir(company_path):

            company_dict = {} 
            
            for filename in os.listdir(company_path):
                
                file_path = os.path.join(company_path, filename)

                df = pl.read_parquet(file_path)
                
                doc_len = df.shape[0]

                df = df.join(sentiment_words, on='column_0', how='inner')

                report_lst = df.get_column(df.columns[0]).to_list()

                match = date_pattern.search(file_path)
                report_date = match.group(1)

                date_and_len = f'{report_date}_{doc_len}'

                company_dict[date_and_len] = report_lst
               
            dict_with_all_companies[company_dir] = make_texts_same_len(company_dict)
    
    return dict_with_all_companies


def save_to_parquet(company_name, company_dict, base_directory):

    match = re.search(r'\\([^\\]*)$', base_directory)

    drectory_name = match.group(1) if match else None

    df = pl.DataFrame(company_dict)

    # Determine the output directory and file name
    output_dir = os.path.join('prepared_data', drectory_name)
    os.makedirs(output_dir, exist_ok=True)

    file_name_new = f"{company_name}_reports.parquet"
    full_path = os.path.join(output_dir, file_name_new)
    full_path = os.path.normpath(full_path)

    print(f"Attempting to write to: {full_path}")

    # Write the DataFrame to Parquet
    df.write_parquet(full_path)

    print(f"{full_path} created successfully")
                    
            

