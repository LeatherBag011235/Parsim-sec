from utils import getUrl, getDocument, getUrls
from consts import COMPANY_NAME_LIST

def main():
    urlPath = getUrl('apple')
    soup = getDocument(urlPath)
    #urlList = getUrls(soup)
    print(soup)
    #print(soup.find(id="edgar-short-form").text)

if __name__ == '__main__':
    main()