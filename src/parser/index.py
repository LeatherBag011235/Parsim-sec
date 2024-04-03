import sys
sys.path.append('/Users/dmitry/Documents/Projects/Parsim-sec/src/parser')

from utils import *

def get_company_links_object():
    company_links_object = {}
    
    driver = createDriver()
    parse_all_links(driver, company_links_object)
    
    return company_links_object