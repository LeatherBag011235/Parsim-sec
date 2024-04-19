import re
from bs4 import BeautifulSoup
from sec_downloader import Downloader
import sec_parser as sp

HEADER_FIRST = "Management’s Discussion"
HEADER_SECOND = "Quantitative and Qualitative"

def get_html(ticker, form):
    
    dl = Downloader("MyCompanyName", "email@example.com")
    html = dl.get_filing_html(ticker=ticker, form=form)

    return html
#get_html("AAPL", "10-Q")

def get_internal_links():    
    #with open ('/Users/dmitry/Documents/Projects/parser_project/raw_files/Apple%2520Inc.%2520(AAPL)%2520(CIK%25200000320193)/2023-08-04_2023-07-01') as fileX:        
        #text = fileX.read()
        
        soup = BeautifulSoup(get_html("AAPL", "10-Q"), 'html.parser')
        
        
        links = soup.find_all('a', href=lambda x: x and x.startswith('#'))
        headers_list = []
        
        for link in links:
            tr = link.find_parent('tr')
            tr_text = tr.get_text()
            
            if(HEADER_FIRST in tr_text or HEADER_SECOND in tr_text):
                headers_list.append(link.get('href')[1:])

        headers_list = list(set(headers_list))
        
        header_first = soup.find(id=headers_list[0])
        header_second = soup.find(id=headers_list[1])
        
        if HEADER_FIRST not in header_first.get_text():
            header_first = header_first.find_next(lambda tag: tag.name and HEADER_FIRST in tag.get_text(strip=True))
            if(header_first == None):
                print('next_element_with_text 1 is None')
        
        if HEADER_SECOND not in header_second.get_text():
            header_second = header_second.find_next(lambda tag: tag.name and HEADER_SECOND in tag.get_text(strip=True))
            if(header_second == None):
                print('next_element_with_text 2 is None')

        text_between_headers = ""
        current_element = header_first        
        while current_element != header_second:
            text_between_headers += current_element.get_text(strip=True) + "\n"
            current_element = current_element.find_next_sibling()
        
        print(text_between_headers)
         
get_internal_links()     
