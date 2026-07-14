import pandas as pd

# ============================================
# LOAD DATASETS
# ============================================

municipality_df = pd.read_csv(
    "data/raw/municipality_master_v2.csv"
)

demand_df = pd.read_csv(
    "data/raw/municipality_equipment_demand.csv"
)

inventory_df = pd.read_csv(
    "data/raw/inventory_master.csv"
)

# Final results list
all_results = []

print("\nSTARTING FULL OPTIMIZATION...\n")

# ============================================
# LOOP THROUGH ALL EQUIPMENT
# ============================================

for _, inventory_row in inventory_df.iterrows():

    equipment_id = inventory_row["equipment_id"]
    equipment_name = inventory_row["equipment_name"]
    available_stock = inventory_row["total_stock"]
    cost_per_unit = inventory_row["cost_per_unit"]

    print("Processing:", equipment_name)

    # Demand for current equipment
    equipment_demand = demand_df[
        demand_df["equipment_id"] == equipment_id
    ]

    # Merge municipality info
    merged_df = pd.merge(
        equipment_demand,
        municipality_df,
        left_on="municipality",
        right_on="municipality_name"
    )

    # ========================================
    # PRIORITY SCORE
    # ========================================

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

    # Sort
    merged_df = merged_df.sort_values(
        by="priority_score",
        ascending=False
    )

    total_priority = merged_df["priority_score"].sum()

    # ========================================
    # ALLOCATION
    # ========================================

    for _, row in merged_df.iterrows():

        demand = row["predicted_demand"]

        allocation = round(
            (row["priority_score"] / total_priority)
            * available_stock
        )

        # IMPORTANT FIX
        if allocation > demand:
            allocation = demand

        total_cost = allocation * cost_per_unit

        all_results.append({

            "municipality": row["municipality"],

            "equipment_id": equipment_id,

            "equipment_name": equipment_name,

            "demand": demand,

            "allocated": allocation,

            "priority_score": round(
                row["priority_score"], 2
            ),

            "cost": total_cost
        })

# ============================================
# SAVE OUTPUT
# ============================================

result_df = pd.DataFrame(all_results)

result_df.to_csv(

    "data/raw/optimized_allocation.csv",

    index=False

)

# ============================================
# SUMMARY
# ============================================

print("\n=================================")
print("OPTIMIZATION COMPLETE")
print("=================================")

print("Total Rows Generated:",
      len(result_df))

print("\nRandom Sample:\n")

print(

    result_df.sample(20)

)
