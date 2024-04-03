import time
import sys

sys.path.append('/Users/dmitry/Documents/Projects/Parsim-sec')

from src.parser.index import get_company_links_object
from src.downloader.index import download_files
from src.converter.index import convert_files

start_time = time.time()

def main():
    company_links_object = get_company_links_object()
    download_files(company_links_object)
    convert_files()
    
if __name__ == '__main__':
    main()

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")