import os
import re
from bs4 import BeautifulSoup as bs
import polars as pl
import numpy as np 
import datetime
from .consts import DATE_REGEX

# проходит по папкам в ./raw_files и собирает названия файлов из этих папок в словарь
def get_date(file_link):
    dates = re.findall(DATE_REGEX, file_link)
    date1 = datetime.datetime.strptime(dates[0], "%Y-%m-%d")
    return date1

def get_object():
    result_obj = {}

    for root, dirs, files in os.walk("./raw_files", topdown=False):
        files = [f for f in files if f != '.DS_Store']
        
        if files:
            relative_dir = os.path.relpath(root, "./raw_files")
            
            if relative_dir == '.':
                continue
            
            files_list = [os.path.join(root, name) for name in files]
            files_list.sort(key = lambda file_link : get_date(file_link))
            result_obj[relative_dir] = files_list

    return result_obj

def process_text(company_name, file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        soup = bs(file, 'html.parser')
        divs = soup.find_all('div')
        text = ''
        
        for div in divs:
            text += div.text
        
        # Clean the text
        text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
        text = re.sub(r'\b\S*?\d\S*\b', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        

        date_pattern = r'\d{4}-\d{2}-\d{2}'
        dates = re.findall(date_pattern, file_name)
        date1 = datetime.datetime.strptime(dates[0], "%Y-%m-%d")
        filed = date1.strftime("%Y-%m-%d")
        date2 = datetime.datetime.strptime(dates[1], "%Y-%m-%d")
        reporting_for = date2.strftime("%Y-%m-%d")

        text = f'{company_name} {filed} {reporting_for}' + ' ' + text
    
    return text

def make_texts_same_len(texts):
    list_of_lists = [string.split() for string in texts]
    max_length = max(len(sub_list) for sub_list in list_of_lists)
    padded_lists_of_lists = [sub_list + [np.nan] * (max_length - len(sub_list)) for sub_list in list_of_lists]
    return padded_lists_of_lists

def save_to_parquet(company_name, texts):
    padded_lists_of_lists = make_texts_same_len(texts)

    df = pl.DataFrame()

    list_of_series = [pl.Series(sub_list[1], sub_list) for i, sub_list in enumerate(padded_lists_of_lists)]
    df = pl.DataFrame({}).hstack(list_of_series)

    # Determine the output directory and file name
    output_dir = os.path.join('.', 'cleared_files')
    os.makedirs(output_dir, exist_ok=True)

    file_name_new = f"{company_name}_reports.parquet"
    full_path = os.path.join(output_dir, file_name_new)
    full_path = os.path.normpath(full_path)

    print(f"Attempting to write to: {full_path}")

    # Write the DataFrame to Parquet
    df.write_parquet(full_path)

    print(f"{full_path} created successfully")