import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/municipality_data.csv")

# Classification logic
def classify(population):
    if population > 3000000:
        return "Metro"
    elif population > 1000000:
        return "Large"
    elif population > 500000:
        return "Medium"
    else:
        return "Small"

# Create new column
df["category"] = df["population"].apply(classify)

# Show results
print(df[["municipality", "population", "category"]])
