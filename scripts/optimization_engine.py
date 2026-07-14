import pandas as pd

# ==========================
# Load datasets
# ==========================

demand_df = pd.read_csv("data/raw/demand_data.csv")
inventory_df = pd.read_csv("data/raw/inventory_data.csv")


# ==========================
# Equipment mapping
# ==========================

equipment_columns = {
    "Garbage Trucks": "garbage_trucks_needed",
    "Road Sweepers": "road_sweepers_needed",
    "Water Tankers": "water_tankers_needed",
    "Drain Cleaners": "drain_cleaners_needed"
}


# ==========================
# Start optimization
# ==========================

grand_total_cost = 0
grand_original_cost = 0

for equipment, demand_column in equipment_columns.items():

    print("\n==========================================")
    print("EQUIPMENT:", equipment)
    print("==========================================")

    # Total demand for this equipment
    total_demand = demand_df[demand_column].sum()

    # Available stock
    available_stock = inventory_df.loc[
        inventory_df["equipment"] == equipment,
        "available_units"
    ].values[0]

    # Cost per unit
    cost_per_unit = inventory_df.loc[
        inventory_df["equipment"] == equipment,
        "cost_per_unit"
    ].values[0]

    print("Total Demand:", total_demand)
    print("Available Stock:", available_stock)

    total_cost = 0

    print("\nAllocation:\n")

    # Municipality allocation
    for index, row in demand_df.iterrows():

        municipality = row["municipality"]
        demand = row[demand_column]

        allocated = (demand / total_demand) * available_stock

        allocation_cost = round(allocated) * cost_per_unit
        total_cost += allocation_cost

        print(
            municipality,
            "→ Demand:", demand,
            "| Allocated:", round(allocated),
            "| Cost: ₹", allocation_cost
        )

    # Cost analysis
    original_cost = total_demand * cost_per_unit
    saved_money = original_cost - total_cost

    grand_total_cost += total_cost
    grand_original_cost += original_cost

    print("\nCost Summary for", equipment)
    print("Optimized Cost: ₹", total_cost)
    print("Original Cost: ₹", original_cost)
    print("Saved: ₹", saved_money)


# ==========================
# Final project summary
# ==========================

grand_saved = grand_original_cost - grand_total_cost

print("\n==========================================")
print("FINAL PROJECT SUMMARY")
print("==========================================")

print("Total Optimized Cost: ₹", grand_total_cost)
print("Total Original Cost: ₹", grand_original_cost)
print("Total Money Saved: ₹", grand_saved)