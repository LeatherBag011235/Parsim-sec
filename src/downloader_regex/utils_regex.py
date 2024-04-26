import os
import re
from bs4 import BeautifulSoup
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


def text_preprocessing(soup):

    text = soup.get_text()
    text = unidecode.unidecode(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


pattern_mnda = r"(?i)item\s+\d+[A-Za-z]?\.?\s*(?:--|[-—])?\s*management[’'`]s\s+discussion\s+and\s+analysis\s+of\s+financial\s+condition\s+and\s+results\s+of\s+operations"
pattern_qnq = r"(?i)item\s+\d+[A-Za-z]?\.?\s*(?:--|[-—])?\s*quantitative\s+and\s+qualitative\s+disclosures\s+about\s+market\s+risk"

#accounting for either order patterns
#pattern_mnda = r"(?i)item\s+\d+[A-Za-z]?\.?\s*(?:--|[-—])?\s*management[’'`]s\s+discussion\s+and\s+analysis\s+of\s+(?:financial\s+condition\s+and\s+results\s+of\s+operations|results\s+of\s+operations\s+and\s+financial\s+condition)"
#pattern_qnq = r"(?i)item\s+\d+[A-Za-z]?\.?\s*(?:--|[-—])?\s*(?:quantitative\s+and\s+qualitative|qualitative\s+and\s+quantitative)?\s+disclosures\s+about\s+market\s+risk"

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
    
    return longest_substring


def clean_text(text):
    
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    text = re.sub(r'\b\S*?\d\S*\b', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    return text 

def save_file(text, company_name, filed_date):
                
                
    file_name = f'{filed_date}' 

    if not os.path.exists('./raw_data./cleared_strings'):
        os.makedirs('./raw_data./cleared_strings')

    if not os.path.exists(f'./raw_data./cleared_strings/{company_name}'):
        os.makedirs(f'./raw_data./cleared_strings/{company_name}')

    with open(f"./raw_data./cleared_strings/{company_name}/{file_name}", "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Page {company_name}/{file_name} saved successfully.")
