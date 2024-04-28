import time

from parser.index import get_company_links_object

#from downloader.index import download_files
#from downloader_regex.index import download_files 
from downloader_regex_full_text.index import download_files

#from converter.index import convert_files
from converter_regex.index import convert_files

start_time = time.time()

files_to_convert = 'full_10Q_10K_without_tabels'

def main():
    company_links_object = get_company_links_object()
    download_files(company_links_object)
    convert_files(files_to_convert)
    
if __name__ == '__main__':
    main()

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")