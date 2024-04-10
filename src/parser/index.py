from utils import *

def get_company_links_object():
    company_links_object = {}
    
    driver = create_driver()
    parse_all_links(driver, company_links_object)
    
    return company_links_object