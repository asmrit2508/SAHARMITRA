import pandas as pd

# Load data
df = pd.read_csv("data/raw/municipality_data.csv")


# Dynamic formula function
def calculate_equipment(row):

    garbage_trucks = round(
        (row["population"] / 50000)
        +
        (row["waste_tons_day"] / 100)
    )

    road_sweepers = round(
        row["road_length_km"] / 100
    )

    water_tankers = round(
        row["population"] / 150000
    )

    drain_cleaners = round(
        row["wards"] / 8
    )

    return {
        "Garbage Trucks": garbage_trucks,
        "Road Sweepers": road_sweepers,
        "Water Tankers": water_tankers,
        "Drain Cleaners": drain_cleaners
    }


# Print recommendations
for index, row in df.iterrows():

    equipment = calculate_equipment(row)

    print("\nMunicipality:", row["municipality"])
    print("Dynamic Allocation:", equipment)