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


company_links_object = {}

def createDriver():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    return driver

cik_re = re.compile(r'\(CIK%2520(\d+)\)')

def extract_cik(name):
    match = cik_re.search(name)
    if match:
        return match.group(1)
    return None

def getUrl(name):
    cik = extract_cik(name)
    urlPath = f'https://www.sec.gov/edgar/search/#/category=custom&ciks={cik}&entityName={name}&forms=10-K%252C10-Q'
    return urlPath

def open_first_page(driver, urlPath):
    driver.get(urlPath)

def get_all_rows(driver):
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "searching-overlay"))
    )
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "preview-file"))
    )
    
    rows = []
    trList  = driver.find_elements(By.CSS_SELECTOR, '#results #hits .table tbody tr')
    
    for tr in trList:        
        page_link = tr.find_element(By.CSS_SELECTOR, 'td.filetype a')
        filed_date = tr.find_element(By.CSS_SELECTOR, 'td.filed').get_attribute('innerText')
        reporting_for = tr.find_element(By.CSS_SELECTOR, 'td.enddate').get_attribute('innerText')
        
        raw_link_data = {
            'page_link': page_link,
            'filed_date': filed_date,
            'reporting_for': reporting_for,
        }
        
        rows.append(raw_link_data)
    
    return rows
    

def getAllModalButtonsOnPage(driver):
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "searching-overlay"))
    )
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "preview-file"))
    )
    buttonList = driver.find_elements(By.CLASS_NAME, "preview-file")

    page_links = []

    for button in buttonList:
        print()
        button_label_is_valid = button.get_attribute('innerText').split()[0] == '10-Q'
        if button_label_is_valid:
            page_links.append(getDocumentLink(driver, button))
    
    return page_links

def getDocumentLink(driver, open_modal_button):
    open_modal_button.click()
    link_to_the_file_element = driver.find_element(By.ID, "open-file")
    link_to_the_file = link_to_the_file_element.get_attribute('href')
    close_modal_button = driver.find_element(By.ID, "close-modal")
    close_modal_button.click()
    return link_to_the_file

def get_company_links(driver, company_name):
    urlPath = getUrl(company_name)
    open_first_page(driver, urlPath)
    first_page_links = getAllModalButtonsOnPage(driver)
#    pages_links = go_throw_pages(driver)
    result = first_page_links #+ pages_links
    #print(result)
    company_name = '_'.join(company_name.split('%2520')).lower()
    #print(company_name)
    company_links_object[company_name] = result

def get_company_links_2(driver, company_name):
    urlPath = getUrl(company_name)
    open_first_page(driver, urlPath)
    links_and_dates = get_all_rows(driver)
    
    for raw_link_object in links_and_dates:
        open_modal_button = raw_link_object['page_link']
        url = getDocumentLink(driver, open_modal_button)
        raw_link_object['page_link'] = url
    
    company_links_object[company_name] = links_and_dates

def parse_all_links(driver):
    for company_name in COMPANY_NAME_LIST:
        get_company_links_2(driver, company_name)
    print(len(company_links_object))
    
    

def download_file_2(company_name, url, filed_date, reporting_for):
    
    def get_random_headers():
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        return headers
    
    with requests.Session() as session:
        #response = session.get(url, headers=get_random_headers())

        #if response.status_code == 200:
        attempts = 3
        for attempt in range(attempts):
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
                print(f"Attempt {attempt + 1} of {attempts} failed; retrying after delay...")
                time.sleep(3) 
        else:
            print(f"Failed to download the page. Status code: {response.status_code}")


def download_files_2():
    for key in company_links_object.keys():
        for item_obj in company_links_object[key]:
            download_file_2(key, item_obj['page_link'], item_obj['filed_date'], item_obj['reporting_for'])

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

def get_date(file_link):
    date_pattern = r'\d{4}-\d{2}-\d{2}'
    dates = re.findall(date_pattern, file_link)
    date1 = datetime.datetime.strptime(dates[0], "%Y-%m-%d")
    return date1

def convert_to_txt(company_name, file_name):
    with open(file_name) as file:
        soup = bs(file, 'html.parser')
        divs = soup.find_all('div')
        text = ''
        
        for div in divs:
            text += div.text
            
        text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
        text = re.sub(r'\b\S*?\d\S*\b', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()

        if not os.path.exists('./cleared_files'):
            os.makedirs('./cleared_files')

        if not os.path.exists(f'./cleared_files/{company_name}'):
            os.makedirs(f'./cleared_files/{company_name}')
        
        file_name_new = file_name.split('/')[-1]
        file_name_new = file_name_new.split('.')[0] + '.txt'
        
        with open(f"./cleared_files/{company_name}/{file_name_new}", "w", encoding="utf-8") as f:
                f.write(text)

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

def make_texts_same_len(texts):
    list_of_lists = [string.split() for string in texts]
    max_length = max(len(sub_list) for sub_list in list_of_lists)
    padded_lists_of_lists = [sub_list + [np.nan] * (max_length - len(sub_list)) for sub_list in list_of_lists]
    return padded_lists_of_lists

def convert_files():
    obj = get_object()
    
    for key, items in obj.items():
        texts = [process_text(key, item) for item in items]
        save_to_parquet(key, texts)