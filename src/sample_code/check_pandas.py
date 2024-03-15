import polars as pl

#df_apple = pl.read_parquet(r'C:\Users\310\Desktop\Progects_Py\cleared_files\apple_reports.parquet')
df_apple = pl.read_parquet(r'/Users/dmitry/Documents/Projects/Parsim-sec/cleared_files/Apple%2520Inc.%2520(AAPL)%2520(CIK%25200000320193)_reports.parquet')

#print(df_apple.select(pl.col("*")))

#df_gm = pl.read_parquet(r'C:\Users\310\Desktop\Progects_Py\cleared_files\general_motors_reports.parquet')

print(df_apple.select(pl.col("*")))