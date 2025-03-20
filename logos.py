import pandas as pd
df = pd.read_parquet("logos.snappy.parquet")
print(df.head())