import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/municipality_data.csv")

# Keep only numerical columns
numeric_df = df.drop("municipality", axis=1)

# Correlation
correlation = numeric_df.corr()

print("\nCorrelation Matrix:\n")
print(correlation)