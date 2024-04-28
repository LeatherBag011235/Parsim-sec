import requests
import polars as pl
from fake_useragent import UserAgent
import json


def get_random_headers():
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    return headers


import requests
from bs4 import BeautifulSoup

def download_report(cik, year, qtr, report_type):
    base_url = "https://www.sec.gov/Archives/edgar/full-index"
    index_url = f"{base_url}/{year}/QTR{qtr}/master.idx"
    
    # Fetch the master index file
    response = requests.get(index_url, headers=get_random_headers())
    lines = response.text.splitlines()
  

    for line in lines:
        parts = line.split('|')

        
        if (len(parts) > 4):
            print(parts)
            print(parts[3], parts[4])
            form_type, company_cik, date_filed, filename = parts[2], parts[4], parts[3], parts[4]
            if company_cik == cik and form_type in report_type:
                # Construct the URL to download the report
                report_url = f"https://www.sec.gov/Archives/{filename}"
                report_response = requests.get(report_url)
                
                # Save the report
                with open(f"{company_cik}_{form_type}_{date_filed}.txt", 'wb') as f:
                    f.write(report_response.content)
                print(f"Downloaded {form_type} for {company_cik} filed on {date_filed}")

# Example usage
cik = '0000320193'  # Apple's CIK
year = '2020'
qtr = '1'
report_types = ['10-Q', '10-K']
res = download_report(cik, year, qtr, report_types)
print(res)
