import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Load dataset
df = pd.read_csv("data/raw/municipality_data.csv")

# Features
X = df[[
    "population",
    "area_km2",
    "waste_tons_day",
    "road_length_km",
    "wards"
]]

# Store inertia values
inertia = []

# Test K values
for k in range(1, 7):

    model = KMeans(
        n_clusters=k,
        random_state=42
    )

    model.fit(X)

    inertia.append(model.inertia_)

# Print values
print("Inertia values:", inertia)

# Plot graph
plt.plot(range(1, 7), inertia, marker="o")

plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia")
plt.title("Elbow Method")

plt.grid(True)
plt.show()