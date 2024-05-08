import requests
import polars as pl
from fake_useragent import UserAgent
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_random_headers():
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    return headers

def get_cik():
    link = (
        #"https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks"
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    )
    df = pd.read_html(link, header=0)[0]
    df = df.astype(str)
    #print(type(str_ciks[0]))
    #cik_set = set(str_df["CIK"])
    #print(snp_str_df)
    df['Count'] = df.groupby('CIK').cumcount()

    qnique_cik = df[df['Count'] == 0]

    snp_str_df = qnique_cik.drop(columns=['Count'])

    return snp_str_df

def download_report(year, qtr):
    base_url = "https://www.sec.gov/Archives/edgar/full-index"
    index_url = f"{base_url}/{year}/QTR{qtr}/xbrl.idx"
    
    # Fetch the master index file
    response = requests.get(index_url, headers=get_random_headers())
    print(response)
    lines = response.text.splitlines()

    return lines


  
def get_all_links(lines):
    #print(type(lines))

    #df = pd.DataFrame(lines, columns=['CIK', 'Name', 'Type', 'Fild_date', 'File' 'value'])
    #print(lines)
    #df_lines

    report_releas_lst = []

    for line in lines:
        part = line.split('|')
        report_releas_lst.append(part)
    
    return report_releas_lst
    

def get_snp_links(report_releas_lst):

    snp_str_df = get_cik()

    reports_list = []

    for sublist in report_releas_lst:

        if (sublist[0] in set(snp_str_df["CIK"])) and (sublist[2] in {'10-K', '10-Q'}):
            res_list = []

            ticker = snp_str_df.loc[snp_str_df["CIK"] == sublist[0], "Symbol"].item()


            res_list.append(ticker)
            res_list.extend(sublist)

            reports_list.append(res_list)
            #if len(sublist) < 5:
            #    print(sublist)

    snp_quarter_df = pd.DataFrame(reports_list, columns=['ticker', 'cik', 'name', 'type', 'fild_date', 'file'])
    #print(snp_quarter_df['name'].count())
    return snp_quarter_df

def get_links_n_dates(snp_quarter_df, company_name):
    links_n_dates = []

    subset_df = snp_quarter_df[snp_quarter_df['ticker'] == company_name].copy()
    subset_df['fild_date'] = pd.to_datetime(subset_df['fild_date'], format='%Y-%m-%d')

    sorted_df = subset_df.sort_values(by='fild_date', ascending=False)
    sorted_df["fild_date"] = sorted_df["fild_date"].astype(str)

    for row in sorted_df.itertuples():
        row_dict = {}
        
        row_dict['page_link'] = row.file
        row_dict['filed_date'] = row.fild_date

        links_n_dates.append(row_dict)

    return links_n_dates



def company_links_obj(snp_quarter_df):
    company_links_object = {}

    company_names = snp_quarter_df['ticker'].unique()

    for company_name in company_names:
        links_n_dates = get_links_n_dates(snp_quarter_df, company_name)
        
        company_links_object[company_name] = links_n_dates

    return company_links_object
    

    


    #needed_companies = [sublist for sublist in report_releas_lst if sublist[0] in snp_ciks_set]

    #print(len(reports_list))

        
        #if (len(parts) > 4):
        #    print(parts)
        #    print(parts[3], parts[4])
        #    form_type, company_cik, date_filed, filename = parts[2], parts[4], parts[3], parts[4]
        #    if company_cik == cik and form_type in report_type:
        #        # Construct the URL to download the report
        #        report_url = f"https://www.sec.gov/Archives/{filename}"
        #        report_response = requests.get(report_url, headers=get_random_headers())
        #        
        #        # Save the report
        #        with open(f"{company_cik}_{form_type}_{date_filed}.txt", 'wb') as f:
        #            f.write(report_response.content)
        #        print(f"Downloaded {form_type} for {company_cik} filed on {date_filed}")
#
# Exampl#e usage
cik = '0000320193'  # Apple's CIK
year = '2020'
qtr = '1'
report_types = ['10-Q', '10-K']

lines = download_report(year, qtr)

report_releas_lst = get_all_links(lines)

snp_quarter_df = get_snp_links(report_releas_lst)

company_links_object = company_links_obj(snp_quarter_df)
print(company_links_object)

