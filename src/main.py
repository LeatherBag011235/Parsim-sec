# from utils import *
from downloader.index import download_files
import time

start_time = time.time()

def main():
    # driver = createDriver()
    # parse_all_links(driver)
    # download_files_2()
    # convert_files()
    # get_object()
    download_files([1, 2, 3])
    # print(get_date('./raw_files/Apple%2520Inc.%2520(AAPL)%2520(CIK%25200000320193)/2020-05-01_2020-03-28'))
if __name__ == '__main__':
    main()

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")