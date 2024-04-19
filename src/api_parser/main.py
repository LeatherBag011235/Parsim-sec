import re
from bs4 import BeautifulSoup, Tag
#from sec_downloader import Downloader
#import sec_parser as sp

HEADER_FIRST = "Management’s Discussion"
HEADER_SECOND = "Quantitative and Qualitative"

#def get_html(ticker, form):
#    
#    dl = Downloader("MyCompanyName", "email@example.com")
#    html = dl.get_filing_html(ticker=ticker, form=form)
#
#    return html
#get_html("AAPL", "10-Q")

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def get_internal_links():    
    with open ('/Users/dmitry/Documents/Projects/parser_project/raw_files/Apple%2520Inc.%2520(AAPL)%2520(CIK%25200000320193)/2023-08-04_2023-07-01') as fileX:        
        text = fileX.read()
        
        #soup = BeautifulSoup(get_html("AAPL", "10-Q"), 'html.parser')
        soup = BeautifulSoup(text, 'html.parser')
        
        links = soup.find_all('a', href=lambda x: x and x.startswith('#'))
        headers_list = []
        
        for link in links:
            tr = link.find_parent('tr')
            tr_text = tr.get_text()
            
            if(HEADER_FIRST in tr_text or HEADER_SECOND in tr_text):
                headers_list.append(link.get('href')[1:])

        headers_list = f7(headers_list)
        
        header_first = soup.find(id=headers_list[0])
        header_second = soup.find(id=headers_list[1])
        
        if HEADER_FIRST not in header_first.get_text():
            prev_element = header_first
            header_first = header_first.find_next(lambda tag: tag.name and HEADER_FIRST in tag.get_text(strip=True))
            if(header_first == None):
                print('\n')
                print(f'header list is: {headers_list}')
                print(f'prev element is: {prev_element}; next element is: {header_second}')
                print('next_element_with_text 1 is None')
                print('\n')
        
        if HEADER_SECOND not in header_second.get_text():
            header_second = header_second.find_next(lambda tag: tag.name and HEADER_SECOND in tag.get_text(strip=True))
            if(header_second == None):
                print('next_element_with_text 2 is None')

        text_between_headers = ""
        current_element = header_first        
        while current_element != header_second:
            should_skip = False
            if current_element.name == 'table':
                #print('SKIPED!!!')
                continue
            first_tag_child = None
            for child in current_element.contents:
                if isinstance(child, Tag):
                    first_tag_child = child
                    if first_tag_child.name == 'table':
                        #print('SKIPED!!!')
                        should_skip = True
                    break
            if should_skip == False:
                text_between_headers += current_element.get_text(strip=True) + "\n"
                #print('basic...')
            current_element = current_element.find_next_sibling()
            #print('\n')
            
        text_between_headers = text_between_headers.replace('\t', '').strip()
        text_between_headers = text_between_headers.replace('\n', '').strip()
        text_between_headers = re.sub(r'[^a-zA-Z\s]', '', re.sub(r'\d+', '', text_between_headers))
        text_between_headers = re.sub(' {1,}', ' ', text_between_headers)
        print(text_between_headers)
         
get_internal_links()     