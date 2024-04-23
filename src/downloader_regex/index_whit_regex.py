from .utils_regex import *

def download_files(company_links_object):
    fails = 0
    mnda_text_list = []
    len_list = []
    all_docs_procesed = 0 

    for key in company_links_object.keys():
        for item_obj in company_links_object[key]:

            all_docs_procesed +=1

            soup = get_soup(key, item_obj['page_link'])
            text = text_preprocessing(soup)
            if check_for_finding_titles(text, key, item_obj['page_link']) == False:
                fails += 1
                continue
            mnda_text, len_of_mnda_text = find_longest_substring(text)

            mnda_text_list.append(mnda_text)
            len_list.append(len_of_mnda_text)

    print(f'Fails over all docs procesed: {fails/all_docs_procesed}')
    print(f'Average len of text {sum(len_list)/all_docs_procesed}')

    return 
         


            