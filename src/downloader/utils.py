import os
from fake_useragent import UserAgent
import requests
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

                if not os.path.exists('./raw_data./full_doc_dirty'):
                    os.makedirs('./raw_data./raw_files')

                if not os.path.exists(f'./raw_data./full_doc_dirty/{company_name}'):
                    os.makedirs(f'./raw_data./full_doc_dirty/{company_name}')

                with open(f"./raw_data./full_doc_dirty/{company_name}/{file_name}", "w", encoding="utf-8") as f:
                    f.write(page_content)

                print(f"Page {company_name}/{file_name} downloaded successfully.")
                break  
            except requests.exceptions.ConnectTimeout:
                print(f"Attempt {attempt + 1} of {ATTEMPTS_AMOUNT} failed; retrying after delay...")
                time.sleep(3) 