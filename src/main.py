from utils import *

def main():
    driver = createDriver()
    parse_all_links(driver)
    #download_file('apple', 'https://www.sec.gov/Archives/edgar/data/1418121/000095017024018793/aple-20231231.htm')
    download_files()

if __name__ == '__main__':
    main()