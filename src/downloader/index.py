from .utils import *

def download_files(company_links_object):
    for key in company_links_object.keys():
        for item_obj in company_links_object[key]:
            download_file(key, item_obj['page_link'], item_obj['filed_date'], item_obj['reporting_for'])