import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from consts import COMPANY_NAME_LIST
import requests
from bs4 import BeautifulSoup as bs
import polars as pl

company_links_object = {}

def createDriver():
    driver = webdriver.Firefox()
    return driver

def getUrl(name):
    urlPath = f'https://www.sec.gov/edgar/search/#/category=form-cat1&entityName={name}'
    return urlPath

def open_firt_page(driver, urlPath):
    driver.get(urlPath)

def check_if_switch_page_is_possible(driver):
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "searching-overlay"))
    )
    next_page_button_container = driver.find_element(By.CSS_SELECTOR, ".pagination li:last-child")

    if 'disabled' in next_page_button_container.get_attribute('class'): 
        return False, False
    
    next_page_button = driver.find_element(By.CSS_SELECTOR, "a[data-value='nextPage']")
    return 'disabled' not in next_page_button.get_attribute('class').split(), next_page_button

def switch_page(driver, switch_button):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(switch_button)).click()
        
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

def go_throw_pages(driver):
    is_page_switch_possible, next_page_button = check_if_switch_page_is_possible(driver)

    pages_links = []

    while is_page_switch_possible:
        switch_page(driver, next_page_button)
        pages_links = getAllModalButtonsOnPage(driver)
        is_page_switch_possible, next_page_button = check_if_switch_page_is_possible(driver)
    
    return pages_links

def get_company_links(driver, company_name):
    urlPath = getUrl(company_name)
    open_firt_page(driver, urlPath)
    first_page_links = getAllModalButtonsOnPage(driver)
    pages_links = go_throw_pages(driver)
    result = first_page_links + pages_links
    company_name = '_'.join(company_name.split('%2520')).lower()
    company_links_object[company_name] = result

def parse_all_links(driver):
    for company_name in COMPANY_NAME_LIST:
        get_company_links(driver, company_name)

def download_file(company_name, url):
    headers = {
        'User-Agent': 'Your User-Agent String Here'
    }

    with requests.Session() as session:
        response = session.get(url, headers=headers)

        if response.status_code == 200:
            page_content = response.text
            file_name = url.split('/')[-1]

            if not os.path.exists('./raw_files'):
                os.makedirs('./raw_files')

            if not os.path.exists(f'./raw_files/{company_name}'):
                os.makedirs(f'./raw_files/{company_name}')

            with open(f"./raw_files/{company_name}/{file_name}", "w", encoding="utf-8") as f:
                f.write(page_content)

            print(f"Page {company_name}/{file_name} downloaded successfully.")
        else:
            print(f"Failed to download the page. Status code: {response.status_code}")

def download_files():
    for key in company_links_object.keys():
        for item in company_links_object[key]:
            download_file(key, item)

def get_object():
    result_obj = {}

    for root, dirs, files in os.walk("./raw_files", topdown=False):
        files = [f for f in files if f != '.DS_Store']
        
        if files:
            relative_dir = os.path.relpath(root, "./raw_files")
            
            if relative_dir == '.':
                continue
            
            files_list = [os.path.join(root, name) for name in files]
            result_obj[relative_dir] = files_list

    return result_obj

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

def convert_to_parquet(company_name, file_name):
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
        file_name_new = file_name_new.split('.')[0] + '.parquet'

        values_list = text.split(' ')
        values_series = pl.Series(values_list)
        df = values_series.to_frame(name="Values")
        df.write_parquet(f"./cleared_files/{company_name}/{file_name_new}")

def convert_files():
    obj = get_object()
    
    for key in obj.keys():
        for item in obj[key]:
            convert_to_parquet(key, item)