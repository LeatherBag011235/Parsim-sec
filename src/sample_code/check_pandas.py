import pandas as pd

df = pd.read_html(r'C:\Users\310\Desktop\Progects_Py\raw_files\apple\aapl-20201226.htm')

#print(df)

#df[0].info()
df[0].iloc[:1]
