from utils import *

def main():
    driver = createDriver()
    parse_all_links(driver)
    download_files()

if __name__ == '__main__':
    main()