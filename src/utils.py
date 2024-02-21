from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def createDriver():
    driver = webdriver.Firefox()
    return driver

def getUrl(name):
    urlPath = f'https://www.sec.gov/edgar/search/#/category=form-cat1&entityName={name}'
    return urlPath

def open_firt_page(driver, urlPath):
    driver.get(urlPath)

def check_if_switch_page_is_possible(driver):
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

    for button in buttonList:
        button_label_is_valid = button.get_attribute('innerText').split()[0] == '10-Q'
        if button_label_is_valid:
            print(getDocumentLink(driver, button))

def getDocumentLink(driver, open_modal_button):
    open_modal_button.click()
    link_to_the_file_element = driver.find_element(By.ID, "open-file")
    link_to_the_file = link_to_the_file_element.get_attribute('href')
    close_modal_button = driver.find_element(By.ID, "close-modal")
    close_modal_button.click()
    return link_to_the_file

def go_throw_pages(driver):
    is_page_switch_possible, next_page_button = check_if_switch_page_is_possible(driver)

    while is_page_switch_possible:
        switch_page(driver, next_page_button)
        #getAllModalButtonsOnPage(driver)
        is_page_switch_possible, next_page_button = check_if_switch_page_is_possible(driver)