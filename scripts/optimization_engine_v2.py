import pandas as pd

# =====================================
# LOAD DATASETS
# =====================================

municipality_df = pd.read_csv(
    "data/raw/municipality_master_v2.csv"
)

demand_df = pd.read_csv(
    "data/raw/municipality_equipment_demand.csv"
)

inventory_df = pd.read_csv(
    "data/raw/inventory_master.csv"
)

# =====================================
# TEST EQUIPMENT
# Garbage Compactor Truck = E001
# =====================================

equipment_id = "E001"

# Get demand only for E001
equipment_demand = demand_df[
    demand_df["equipment_id"] == equipment_id
]

# Get inventory for E001
available_stock = inventory_df[
    inventory_df["equipment_id"] == equipment_id
]["total_stock"].values[0]

print("Available Stock:", available_stock)

# =====================================
# MERGE MUNICIPALITY + DEMAND
# =====================================

merged_df = pd.merge(

    equipment_demand,

    municipality_df,

    left_on="municipality",
    right_on="municipality_name"

)

# =====================================
# PRIORITY SCORE
# =====================================

priority_scores = []

for _, row in merged_df.iterrows():

    score = 0

    # Population factor
    score += row["population"] / 1000000

    # Municipality class factor
    if row["municipality_class"] == "Metro":
        score += 5

    elif row["municipality_class"] == "Large":
        score += 3

    elif row["municipality_class"] == "Medium":
        score += 2

    else:
        score += 1

    # Demand factor
    score += row["predicted_demand"]

    priority_scores.append(score)

merged_df["priority_score"] = priority_scores

# =====================================
# SORT BY PRIORITY
# =====================================

merged_df = merged_df.sort_values(

    by="priority_score",

    ascending=False

)

print("\nPriority Ranking:\n")

print(

    merged_df[

        [
            "municipality",
            "predicted_demand",
            "priority_score"
        ]

    ]

)

# =====================================
# ALLOCATION
# =====================================

total_priority = merged_df["priority_score"].sum()

print("\nAllocation:\n")

for _, row in merged_df.iterrows():

    allocation = round(

        (row["priority_score"] / total_priority)

        * available_stock

    )

    print(

        row["municipality"],

        "→ Demand:", row["predicted_demand"],

        "| Allocated:", allocation

    )
    