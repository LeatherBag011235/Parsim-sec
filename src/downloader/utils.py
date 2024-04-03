import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from consts import COMPANY_NAME_LIST
import requests
from bs4 import BeautifulSoup as bs
import polars as pl
import numpy as np 
import datetime
import time

def get_random_headers():
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    return headers

def download_file(company_name, url, filed_date, reporting_for):
    with requests.Session() as session:
        ATTEMPTS_AMOUNT = 3
        for attempt in range(ATTEMPTS_AMOUNT):
            try:
                response = session.get(url, headers=get_random_headers(), timeout=10)

                page_content = response.text
                file_name = f'{filed_date}_{reporting_for}' 

                if not os.path.exists('./raw_files'):
                    os.makedirs('./raw_files')

                if not os.path.exists(f'./raw_files/{company_name}'):
                    os.makedirs(f'./raw_files/{company_name}')

                with open(f"./raw_files/{company_name}/{file_name}", "w", encoding="utf-8") as f:
                    f.write(page_content)

                print(f"Page {company_name}/{file_name} downloaded successfully.")
                break  
            except requests.exceptions.ConnectTimeout:
                print(f"Attempt {attempt + 1} of {ATTEMPTS_AMOUNT} failed; retrying after delay...")
                time.sleep(3) 