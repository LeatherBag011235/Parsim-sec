from selenium import webdriver
from bs4 import BeautifulSoup

def getUrl(name):
    urlPath = f'https://www.sec.gov/edgar/search/#/category=form-cat1&entityName={name}'
    return urlPath

def getDocument(urlPath):
    browser = webdriver.PhantomJS()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'} 
    browser.get(urlPath, headers=headers)
    html = browser.page_source
    #html_text = requests.get(urlPath, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def getUrls(soup):
    urlList = soup.find_all('a', {'class':"preview-file"})
    return urlList