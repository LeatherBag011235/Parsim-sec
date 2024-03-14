from utils import *

def main():
    driver = createDriver()
    open_first_page(driver, 'https://www.sec.gov/edgar/search/#/category=custom&entityName=General%2520Motors%2520Co%2520(GM)%2520(CIK%25200001467858)&forms=10-Q')
    get_all_rows(driver)
    #parse_all_links(driver)
    #download_files()
    #get_object()
    #convert_files()

if __name__ == '__main__':
    main()