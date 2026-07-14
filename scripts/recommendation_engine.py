import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/municipality_data.csv")

# Municipality classifier
def classify(population):
    if population > 3000000:
        return "Metro"
    elif population > 1000000:
        return "Large"
    elif population > 500000:
        return "Medium"
    else:
        return "Small"

df["category"] = df["population"].apply(classify)


# Recommendation rules
def recommend(category):

    if category == "Metro":
        return {
            "Garbage Trucks": 100,
            "Road Sweepers": 15,
            "Water Tankers": 30,
            "Drain Cleaners": 20
        }

    elif category == "Large":
        return {
            "Garbage Trucks": 30,
            "Road Sweepers": 5,
            "Water Tankers": 10,
            "Drain Cleaners": 7
        }

    elif category == "Medium":
        return {
            "Garbage Trucks": 15,
            "Road Sweepers": 2,
            "Water Tankers": 5,
            "Drain Cleaners": 3
        }

    else:
        return {
            "Garbage Trucks": 5,
            "Road Sweepers": 0,
            "Water Tankers": 2,
            "Drain Cleaners": 1
        }


# Print recommendations
for index, row in df.iterrows():

    recommendation = recommend(row["category"])

    print("\nMunicipality:", row["municipality"])
    print("Category:", row["category"])
    print("Recommended Equipment:", recommendation)