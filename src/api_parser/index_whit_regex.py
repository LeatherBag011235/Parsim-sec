from .utils_regex import *

def download_files(company_links_object):
    fails = 0
    for key in company_links_object.keys():
        for item_obj in company_links_object[key]:
            soup = get_soup(key, item_obj['page_link'])
            text = text_preprocessing(soup)
            if check_for_finding_titles(text, key, item_obj['page_link']) == False:
                fails += 1
            res_str = find_longest_substring(text)
            print(res_str)


            