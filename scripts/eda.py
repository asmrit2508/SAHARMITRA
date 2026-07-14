import pandas as pd

# Load dataset
df = pd.read_csv("../data/raw/municipality_data.csv")

# Show dataset
print("Municipality Dataset:\n")
print(df)

print("\n" + "="*50)

# Info
print("\nDataset Information:\n")
print(df.info())

print("\n" + "="*50)

# Statistics
print("\nStatistical Summary:\n")
print(df.describe())