import os
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

def get_internal_links(file):  
    openedFile = open(file, 'r', encoding='utf-8')       
    text = openedFile.read()
    
    #soup = BeautifulSoup(get_html("AAPL", "10-Q"), 'html.parser')
    soup = BeautifulSoup(text, 'html.parser')
    
    links = soup.find_all('a', href=lambda x: x and x.startswith('#'))
    headers_list = []
    
    for link in links:
        tr = link.find_parent('tr')
        if tr == None:
            continue
        tr_text = tr.get_text()
        
        if(HEADER_FIRST in tr_text or HEADER_SECOND in tr_text):
            headers_list.append(link.get('href')[1:])
    headers_list = f7(headers_list)
        
    header_first = soup.find(id=headers_list[0])
    header_second = soup.find(id=headers_list[1])
    
    
    # if HEADER_FIRST not in header_first.get_text():
    #     prev_element = header_first
    #     header_first = header_first.find_next(lambda tag: tag.name and HEADER_FIRST in tag.get_text(strip=True))
    #     if(header_first == None):
    #         print('\n')
    #         print(f'header list is: {headers_list}')
    #         print(f'prev element is: {prev_element}; next element is: {header_second}')
    #         print('next_element_with_text 1 is None')
    #         print('\n')
    
    # if HEADER_SECOND not in header_second.get_text():
    #     header_second = header_second.find_next(lambda tag: tag.name and HEADER_SECOND in tag.get_text(strip=True))
    #     if(header_second == None):
    #         print('next_element_with_text 2 is None')
    
    text_between_headers = ""
    current_element = header_first    
        
    #print('\n')
    #next_element = current_element.find_next_sibling()
    #if next_element == None:
    #    next_element = current_element.parent.find_next_sibling()
    #print(next_element, current_element)
    #print('\n')    
    
    for noscript in soup.find_all('noscript'):
        noscript.decompose()
    
    def check_id_in_string(input_string, header_second_id):
        pattern = re.compile(r'id="' + re.escape(header_second_id) + r'"')
        match = pattern.search(input_string)
        return match is not None
    
    #print(check_id_in_string('<div style="text-align:justify;font-size:9pt;"><a style="font-family:Amplitude;font-size:9pt;" id="sFFB01EC91BE75BE1917C8464373D0E6B"><span style="font-family:Amplitude;font-size:9pt;">Quantitative and Qualitative Disclosures About Market Risk.</span></a></div>', 'sFFB01EC91BE75BE1917C8464373D0E6B'))
    
    while check_id_in_string(current_element.prettify().strip(), header_second['id']) == False:
        #print(current_element)
        #print(current_element.has_attr('id') == False and current_element['id'] != header_second['id'])
        #print('\n\n')
        #print('current_element: ', current_element, '\n', 'header_second: ', header_second)
        #print('\n\n')
        #print(current_element)
        should_skip = False
        if current_element.name == 'table':
            #print('SKIPED!!!')
            should_skip = True
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
        next_element = current_element.find_next_sibling()
        if next_element == None:
            current_element = current_element.parent.find_next_sibling()
        else:
            current_element = current_element.find_next_sibling()
        #print('\n')
        
    text_between_headers = text_between_headers.replace('\t', '').strip()
    text_between_headers = text_between_headers.replace('\n', '').strip()
    text_between_headers = re.sub(r'[^a-zA-Z\s]', '', re.sub(r'\d+', '', text_between_headers))
    text_between_headers = re.sub(' {1,}', ' ', text_between_headers)
    
    return text_between_headers 

def anilise_all_raw_files():
    failed_general = 0
    all_documents_count = 0
    for root, dirs, files in os.walk("./raw_files", topdown=False):
        files = [f'{root}/{f}' for f in files if f != '.DS_Store']
        all_documents_count += len(files)
        
        for file in files:
            print('\n')
            print(f'Testing for the file: {file}')
            try:
                result = get_internal_links(file)
                print(f'{file} - {result}')
                print('Success')
                
            except:
                print('Fail')
                failed_general += 1
            print('\n')
        
    print('\n')
    print(f'Failed: {failed_general / all_documents_count}')

#anilise_all_raw_files()
print(get_internal_links('/Users/dmitry/Documents/Projects/parser_project/raw_files/EXXON%2520MOBIL%2520CORP%2520(XOM)%2520(CIK%25200000034088)/2019-05-02_2019-03-31'))