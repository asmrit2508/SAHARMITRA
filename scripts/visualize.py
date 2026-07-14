import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("data/raw/municipality_data.csv")

# Plot population vs garbage trucks
plt.scatter(df["population"], df["garbage_trucks"])

plt.xlabel("Population")
plt.ylabel("Number of Garbage Trucks")
plt.title("Population vs Garbage Trucks")

plt.show()