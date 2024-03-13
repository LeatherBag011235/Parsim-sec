import polars as pl

df = pl.read_parquet(r'C:\Users\310\Desktop\Progects_Py\cleared_files\apple\apple_texts.parquet')

print(df.select(pl.col("text_26")))


