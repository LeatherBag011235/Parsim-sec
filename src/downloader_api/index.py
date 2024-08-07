from .utils import *


def download_files(company_links_object):

    fails = 0
    len_list = []
    all_docs_procesed = 0 

    session = requests.Session()

    for key in company_links_object.keys():

        for item_obj in company_links_object[key]:

            all_docs_procesed +=1

            soup = get_soup(session, key, item_obj['page_link'])
            soup = delete_tabeles(soup)

            text = text_preprocessing(soup)

            cleaned_mnda_text = clean_text(text)


            if len(cleaned_mnda_text) > 10000:

                print(key, item_obj['filed_date'])

                save_file(cleaned_mnda_text, key, item_obj['filed_date'])
                len_list.append(len(cleaned_mnda_text))

            else:
                print(f" \n {key} \n len of {item_obj['page_link']} less then 10000 characters: {len(cleaned_mnda_text)} \n It is not saved \n")  
        

    print(f'Fails over all docs procesed: {fails/all_docs_procesed}')
    print(f'Average len of text {sum(len_list)/all_docs_procesed}')
    
         


            