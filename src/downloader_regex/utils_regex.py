import os
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import requests
import polars as pl
import numpy as np 
import datetime
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


def text_preprocessing(soup):

    text = soup.get_text()
    text = unidecode.unidecode(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


pattern_mnda = r"(?i)item\s+\d+[A-Za-z]?\.?\s*(?:--|[-—])?\s*management[’'`]s\s+discussion\s+and\s+analysis\s+of\s+financial\s+condition\s+and\s+results\s+of\s+operations"
pattern_qnq = r"(?i)item\s+\d+[A-Za-z]?\.?\s*(?:--|[-—])?\s*quantitative\s+and\s+qualitative\s+disclosures\s+about\s+market\s+risk"


def check_for_finding_titles(text, company_name, url):

    matches_mnda = re.findall(pattern_mnda, text)
    matches_qnq = re.findall(pattern_qnq, text)

    if (len(matches_mnda) > 0) & (len(matches_qnq) > 0 ):
        return True
    else:
        print('\n')
        print(f' !!! Fail to find both titles in {company_name} url: {url}')
        print('\n')
        return False


def find_longest_substring(text):

    matches_mnda = list(re.finditer(pattern_mnda, text))
    matches_qnq = list(re.finditer(pattern_qnq, text))
    
    longest_substring = ""
    
    for mnda_match in matches_mnda:
        mnda_end = mnda_match.end()
      
        for qnq_match in matches_qnq:
            if qnq_match.start() > mnda_end:
                substring = text[mnda_end:qnq_match.start()]
                if len(substring) > len(longest_substring):
                    longest_substring = substring
                break  
    
    return longest_substring, len(longest_substring)

