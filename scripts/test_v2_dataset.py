import pandas as pd

# load new dataset
df = pd.read_csv("data/raw/municipality_master_v2.csv")

# print first 5 rows
print(df.head())

print("\nColumns:")
print(df.columns)

print("\nTotal municipalities:")
print(len(df))