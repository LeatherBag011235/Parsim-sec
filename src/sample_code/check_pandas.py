import polars as pl

df_apple = pl.read_parquet(r'C:\Users\310\Desktop\Progects_Py\cleared_files\apple_reports.parquet')

#print(df_apple.select(pl.col("*")))

df_gm = pl.read_parquet(r'C:\Users\310\Desktop\Progects_Py\cleared_files\general_motors_reports.parquet')

print(df_gm.select(pl.col("*")))