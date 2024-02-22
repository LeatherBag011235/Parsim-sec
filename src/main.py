from utils import *

def main():
    driver = createDriver()
    parse_all_links(driver)
    print(company_links_object)

if __name__ == '__main__':
    main()