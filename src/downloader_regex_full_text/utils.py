import os
import re
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import requests

import time
import unidecode

def get_random_headers():
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    return headers

def get_soup(company_name, url):
    with requests.Session() as session:
        ATTEMPTS_AMOUNT = 3
        for attempt in range(ATTEMPTS_AMOUNT):
            try:
                response = session.get(url, headers=get_random_headers(), timeout=10)

                soup = BeautifulSoup(response.text, 'html.parser')

                print(f"Page {company_name}/{url} downloaded successfully.")

                return soup
            
            
            except requests.exceptions.ConnectTimeout:
                print(f"Attempt {attempt + 1} of {ATTEMPTS_AMOUNT} failed for {url} retrying after delay...")
                time.sleep(3) 

def delete_tabeles(soup):
    for table in soup.find_all('table'):
        table.decompose()
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
                
                
    file_name = f'{filed_date}' 

    if not os.path.exists('./full_10Q_10K_without_tabels'):
        os.makedirs('./full_10Q_10K_without_tabels')

    if not os.path.exists(f'./full_10Q_10K_without_tabels/{company_name}'):
        os.makedirs(f'./full_10Q_10K_without_tabels/{company_name}')

    with open(f"./full_10Q_10K_without_tabels/{company_name}/{file_name}", "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Page {company_name}/{file_name} saved successfully.")
