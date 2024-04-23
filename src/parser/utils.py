
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from .consts import COMPANY_NAME_LIST, CIK_REGEX

# Создаем драйвер
def create_driver():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    return driver

# Вызываем get_company_links для каждой компании
def parse_all_links(driver, company_links_object): 
    for company_name in COMPANY_NAME_LIST:
        get_company_links(driver, company_links_object, company_name)

# Функция для извлечения CIK
def extract_cik(name):
    match = CIK_REGEX.search(name)
    if match:
        return match.group(1)
    return None

# Функция для получения URL
def get_url(name):
    cik = extract_cik(name)
    urlPath = f'https://www.sec.gov/edgar/search/#/category=custom&ciks={cik}&entityName={name}&forms=10-K%252C10-Q'
    return urlPath

# Функция для открытия страницы
def open_page(driver, urlPath):
    driver.get(urlPath)

# Собирает все строки в таблице: ссылка на документ, fieild_date, reporting_for
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

# Функция для открытия модального окна и сохранения ссылки на документ
def getDocumentLink(driver, open_modal_button):
    open_modal_button.click()
    link_to_the_file_element = driver.find_element(By.ID, "open-file")
    link_to_the_file = link_to_the_file_element.get_attribute('href')
    close_modal_button = driver.find_element(By.ID, "close-modal")
    close_modal_button.click()
    return link_to_the_file

# Проходимся по полученным строкам и записываем ссылку на конечный документ, fieild_date и reporting_for в словарь
def get_company_links(driver, company_links_object, company_name):
    urlPath = get_url(company_name)
    open_page(driver, urlPath)
    links_and_dates = get_all_rows(driver)
    
    for raw_link_object in links_and_dates:
        open_modal_button = raw_link_object['page_link']
        url = getDocumentLink(driver, open_modal_button)
        raw_link_object['page_link'] = url
    
    company_links_object[company_name] = links_and_dates

