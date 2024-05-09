import requests
from fake_useragent import UserAgent
import requests
import pandas as pd



#def get_random_headers():
#    ua = UserAgent()
#    headers = {'User-Agent': ua.random}
#    print(headers)
#    return headers


headers = {
    'User-Agent': 'mvshibanov@edu.hse.ru'
}

def get_cik():
    link = (
        #"https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks"
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    )
    df = pd.read_html(link, header=0)[0]
    df = df.astype(str)
    df['Count'] = df.groupby('CIK').cumcount()

    qnique_cik = df[df['Count'] == 0]

    snp_str_df = qnique_cik.drop(columns=['Count'])

    return snp_str_df

def download_report(year, qtr):
    base_url = "https://www.sec.gov/Archives/edgar/full-index"
    index_url = f"{base_url}/{year}/QTR{qtr}/master.idx"
    
    response = requests.get(index_url, headers=headers)
    lines = response.text.splitlines()
    
    return lines


  
def get_all_links(lines):

    report_releas_lst = []

    for line in lines:
        part = line.split('|')
        if len(part) == 5:
            report_releas_lst.append(part)
    print(f'all links prepared. the len: {len(report_releas_lst)}')

    reports_df = pd.DataFrame(report_releas_lst, columns=['cik', 'name', 'type', 'filed_date', 'file'])

    return reports_df
    

def get_snp_links(reports_df):

    snp_str_df = get_cik()
    #unique_ciks = set(snp_str_df["CIK"])
    #reports_list = []

    reports_df = reports_df[reports_df['type'].isin(['10-K', '10-Q'])]
    reports_df.loc[:, 'cik'] = reports_df['cik'].astype(snp_str_df['CIK'].dtype)

    snp_str_df.loc[:, 'CIK'] = pd.to_numeric(snp_str_df['CIK']).astype(int)
    reports_df.loc[:, 'cik'] = pd.to_numeric(reports_df['cik']).astype(snp_str_df['CIK'].dtype)

    snp_str_df.set_index('CIK', inplace=True)

    snp_quarter_df = reports_df.merge(snp_str_df[['Symbol']], left_on='cik', right_index=True, how='inner')
    snp_quarter_df.rename(columns={'Symbol': 'ticker'}, inplace=True)

    snp_quarter_df = snp_quarter_df[['ticker', 'cik', 'name', 'type', 'filed_date', 'file']]
    #for sublist in report_releas_lst:
#
    #    if (sublist[0] in unique_ciks) and (sublist[2] in {'10-K', '10-Q'}):
    #        res_list = []
#
    #        ticker = snp_str_df.loc[snp_str_df["CIK"] == sublist[0], "Symbol"].item()
#
#
    #        res_list.append(ticker)
    #        res_list.extend(sublist)
#
    #        reports_list.append(res_list)
    #print('ready to create a total pd.df')
    #snp_quarter_df = pd.DataFrame(reports_list, columns=['ticker', 'cik', 'name', 'type', 'fild_date', 'file'])
    print('pd df created')
    return snp_quarter_df

def get_links_n_dates(snp_quarter_df, company_name):
    links_n_dates = []

    subset_df = snp_quarter_df[snp_quarter_df['ticker'] == company_name].copy()
    subset_df['filed_date'] = pd.to_datetime(subset_df['filed_date'], format='%Y-%m-%d')

    sorted_df = subset_df.sort_values(by='filed_date', ascending=False)
    sorted_df["filed_date"] = sorted_df["filed_date"].astype(str)

    for row in sorted_df.itertuples():
        row_dict = {}
        
        row_dict['page_link'] = row.file
        row_dict['filed_date'] = row.filed_date

        links_n_dates.append(row_dict)

    return links_n_dates



def compile_links(snp_quarter_df):
    company_links_object = {}

    company_names = snp_quarter_df['ticker'].unique()

    for company_name in company_names:
        
        links_n_dates = get_links_n_dates(snp_quarter_df, company_name)
        
        company_links_object[company_name] = links_n_dates

    return company_links_object


