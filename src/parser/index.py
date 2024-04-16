import sys
sys.path.append('/Users/dmitry/Documents/Projects/Parsim-sec/src/parser')

from .utils import create_driver, parse_all_links



def get_company_links_object():
    company_links_object = {}
    
    driver = create_driver()
    parse_all_links(driver, company_links_object)
    
    return company_links_object