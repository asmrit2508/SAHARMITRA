import pandas as pd
from sklearn.cluster import KMeans

# Load data
df = pd.read_csv("data/raw/municipality_data.csv")

# Features for clustering
X = df[[
    "population",
    "area_km2",
    "waste_tons_day",
    "road_length_km",
    "wards"
]]

# Train KMeans
model = KMeans(
    n_clusters=3,
    random_state=42
)

# Initial clusters (random labels)
df["cluster"] = model.fit_predict(X)

# ---------------------------------------------------
# Step 1: Find average population in each cluster
# ---------------------------------------------------

cluster_means = df.groupby("cluster")["population"].mean()

print("\nAverage population in each raw cluster:\n")
print(cluster_means)

# Example output:
# cluster 0 → avg 400000
# cluster 2 → avg 1200000
# cluster 1 → avg 4500000


# ---------------------------------------------------
# Step 2: Sort clusters by average population
# ---------------------------------------------------

sorted_clusters = cluster_means.sort_values()

# Example:
# old cluster 0 = smallest
# old cluster 2 = medium
# old cluster 1 = largest

# Create mapping
cluster_mapping = {
    sorted_clusters.index[0]: 0,   # Smallest → 0
    sorted_clusters.index[1]: 1,   # Medium → 1
    sorted_clusters.index[2]: 2    # Largest → 2
}


# ---------------------------------------------------
# Step 3: Replace old cluster labels
# ---------------------------------------------------

df["cluster"] = df["cluster"].map(cluster_mapping)


# ---------------------------------------------------
# Step 4: Print final result
# ---------------------------------------------------

print("\nFinal Ordered Clusters:\n")
print(df[["municipality", "population", "cluster"]])