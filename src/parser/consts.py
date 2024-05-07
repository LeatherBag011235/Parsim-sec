import re
COMPANY_NAME_LIST = ['FASTENAL%2520CO%2520(FAST)%2520(CIK%25200000815556)', 'Apple%2520Inc.%2520(AAPL)%2520(CIK%25200000320193)']
#COMPANY_NAME_LIST = ['Apple%2520Inc.%2520(AAPL)%2520(CIK%25200000320193)', 'MICROSOFT%2520CORP%2520(MSFT)%2520(CIK%25200000789019)', 
#                     'BigCommerce%2520Holdings%252C%2520Inc.%2520(BIGC)%2520(CIK%25200001626450)', 'ROKU%252C%2520INC%2520(ROKU)%2520(CIK%25200001428439)', 
#                     'JPMORGAN%2520CHASE%2520(CIK%25200000019617)', 'VISA%2520INC.%2520(V)%2520(CIK%25200001403161)', 
#                     'Block%252C%2520Inc.%2520(SQ%252C%2520BSQKZ)%2520(CIK%25200001512673)', 'Robinhood%2520Markets%252C%2520Inc.%2520(HOOD)%2520(CIK%25200001783879)', 
#                     'JOHNSON%252C%252C%2520JOHNSON%2520(JNJ)%2520(CIK%25200000200406)', 'PFIZER%2520INC%2520(PFE)%2520(CIK%25200000078003)', 
#                     'Moderna%252C%2520Inc.%2520(MRNA)%2520(CIK%25200001682852)', 'Teladoc%2520Health%252C%2520Inc.%2520(TDOC)%2520(CIK%25200001477449)', 
#                     'EXXON%2520MOBIL%2520CORP%2520(XOM)%2520(CIK%25200000034088)', 'CHEVRON%2520CORP%2520(CVX)%2520(CIK%25200000093410)', 
#                     'FIRST%2520SOLAR%252C%2520INC.%2520(FSLR)%2520(CIK%25200001274494)', 'PLUG%2520POWER%2520INC%2520(PLUG)%2520(CIK%25200001093691)', 
#                     'GENERAL%252CELECTRIC%2520CO%2520(GE)%2520(CIK%25200000040545)', '3M%2520CO%2520(MMM)%2520(CIK%25200000066740)', 
#                     'CATERPILLAR%2520INC%2520(CAT)%2520(CIK%25200000018230)', 'FASTENAL%2520CO%2520(FAST)%2520(CIK%25200000815556)']
#
CIK_REGEX = re.compile(r'\(CIK%2520(\d+)\)')
DATE_REGEX = r'\d{4}-\d{2}-\d{2}'