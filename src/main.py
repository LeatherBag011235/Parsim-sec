from utils import *
from consts import COMPANY_NAME_LIST

def main():
    driver = createDriver()
    urlPath = getUrl('apple')
    open_firt_page(driver, urlPath)
    #getAllModalButtonsOnPage(driver)
    go_throw_pages(driver)


if __name__ == '__main__':
    main()