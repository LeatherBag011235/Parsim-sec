import os
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import time
import unidecode
from .consts import start_pattern, end_pattern
import polars as pl

#def get_random_headers():
#    ua = UserAgent()
#    headers = {'User-Agent': ua.random}
#    return headers

headers = {
    'User-Agent': 'mvshibanov@edu.hse.ru'
}

def get_soup(session, company_name, url):
    ATTEMPTS_AMOUNT = 3
    for attempt in range(ATTEMPTS_AMOUNT):
        try:
            ful_url = f'https://www.sec.gov/Archives/{url}'

            response = session.get(ful_url, headers=headers, timeout=10)

            #response = requests.get(url, headers=get_random_headers(), timeout=10)
            content  = response.text

            start_match = start_pattern.search(content)
            if start_match:
                start_idx = start_match.end()
            else:
                print(f'fail to find start idx in {company_name} ==> {ful_url} \n use <html> instead')
                start_match = end_pattern.search(content)

                if start_match:
                    start_idx = start_match.end()
                else:
                    print(f'fail to find start idx with <html> {company_name} ==> {ful_url} \n !!!!!!!!!!!!')

            end_match = end_pattern.search(content, start_idx)
            if end_match:
                end_idx = end_match.end()
            else:
                print(f'fail to find end idx in{company_name} ==> {ful_url}')
        
            html_content = content[start_idx:end_idx]
            soup = BeautifulSoup(html_content, 'html.parser')

            print(f"Page {company_name} ==> {ful_url} paresed successfully.")

            return soup
        
        
        except requests.exceptions.ConnectTimeout:
            print(f"Attempt {attempt + 1} of {ATTEMPTS_AMOUNT} failed for {ful_url} retrying after delay...")
            time.sleep(3) 


def delete_tabeles(soup):

    for script in soup(["script", "style", "head", "title", "meta", "[document]"]):
            script.decompose() 

    for table in soup.find_all('table'):
        table.decompose()
    
    for a in soup.find_all("a"):
        a.decompose()

    return soup


def text_preprocessing(soup):

    text = soup.get_text()
    text = unidecode.unidecode(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def clean_text(text):
    
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    text = re.sub(r'\b\S*?\d\S*\b', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    return text 

def save_file(text, company_name, filed_date):
                
            
    file_name = f'{filed_date}.parquet'
   
    text_col = pl.DataFrame(text.split())

    directory_path = f'./raw_data/full_snp_five_hundred/{company_name}/'

    if not os.path.exists(f'{directory_path}'):
        os.makedirs(f'{directory_path}')

    text_col.write_parquet(os.path.join(directory_path, file_name))

    print(f"Text for {company_name} ==> {os.path.join(directory_path, file_name)} saved successfully.")