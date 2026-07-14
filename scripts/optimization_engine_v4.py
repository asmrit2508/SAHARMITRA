import pandas as pd

# ==========================================
# LOAD DATASETS
# ==========================================

municipality_df = pd.read_csv(
    "data/raw/municipality_master_v2.csv"
)

equipment_df = pd.read_csv(
    "data/raw/equipment_master_v2.csv"
)

demand_df = pd.read_csv(
    "data/raw/municipality_equipment_demand.csv"
)

inventory_df = pd.read_csv(
    "data/raw/inventory_master.csv"
)

all_results = []

print("\nSTARTING INTELLIGENT OPTIMIZATION...\n")

# ==========================================
# LOOP THROUGH ALL EQUIPMENT
# ==========================================

for _, equip in equipment_df.iterrows():

    equipment_id = equip["equipment_id"]
    equipment_name = equip["equipment_name"]

    inventory_row = inventory_df[
        inventory_df["equipment_id"] == equipment_id
    ]

    available_stock = inventory_row[
        "total_stock"
    ].values[0]

    cost_per_unit = inventory_row[
        "cost_per_unit"
    ].values[0]

    equipment_demand = demand_df[
        demand_df["equipment_id"] == equipment_id
    ]

    merged_df = pd.merge(

        equipment_demand,

        municipality_df,

        left_on="municipality",

        right_on="municipality_name"

    )

    priority_scores = []

    # ======================================
    # DYNAMIC SCORING
    # ======================================

    for _, row in merged_df.iterrows():

        score = 0

        # -------------------------------
        # Municipality class
        # -------------------------------

        if row["municipality_class"] == "Metro":
            score += 5

        elif row["municipality_class"] == "Large":
            score += 3

        elif row["municipality_class"] == "Medium":
            score += 2

        else:
            score += 1

        # -------------------------------
        # Dynamic dependency logic
        # -------------------------------

        if equip["depends_population"] == 1:
            score += row["population"] / 1000000

        if equip["depends_waste_generation"] == 1:
            score += row["waste_generation_tpd"] / 100

        if equip["depends_road_network"] == 1:
            score += row["road_network_km"] / 100

        if equip["depends_water_supply"] == 1:
            score += (
                100 -
                row["water_supply_coverage_percent"]
            ) / 10

        if equip["depends_drainage"] == 1:
            score += (
                100 -
                row["drainage_coverage_percent"]
            ) / 10

        if equip["depends_sewerage"] == 1:
            score += (
                100 -
                row["sewerage_coverage_percent"]
            ) / 10

        if equip["depends_flood_risk"] == 1:
            score += row["flood_risk_index"]

        if equip["depends_industrial_activity"] == 1:
            score += row["industrial_activity_index"]

        if equip["depends_construction_activity"] == 1:
            score += row["construction_activity_index"]

        if equip["depends_tourism_activity"] == 1:
            score += row["tourism_activity_index"]

        # -------------------------------
        # Equipment intelligence
        # -------------------------------

        score += equip["criticality_score"] * 2

        score += equip["usage_frequency_score"]

        # Demand factor
        score += row["predicted_demand"]

        priority_scores.append(score)

    merged_df["priority_score"] = priority_scores

    merged_df = merged_df.sort_values(

        by="priority_score",

        ascending=False

    )

    total_priority = merged_df[
        "priority_score"
    ].sum()

    # ======================================
    # ALLOCATION
    # ======================================

    for _, row in merged_df.iterrows():

        demand = row["predicted_demand"]

        allocation = round(

            (
                row["priority_score"]

                / total_priority

            )

            * available_stock

        )

        if allocation > demand:
            allocation = demand

        total_cost = allocation * cost_per_unit

        all_results.append({

            "municipality": row["municipality"],

            "equipment_id": equipment_id,

            "equipment_name": equipment_name,

            "demand": demand,

            "allocated": allocation,

            "priority_score":
                round(
                    row["priority_score"], 2
                ),

            "cost": total_cost
        })

# ==========================================
# SAVE
# ==========================================

result_df = pd.DataFrame(all_results)

result_df.to_csv(

    "data/raw/optimized_allocation_v4.csv",

    index=False

)

print("\n===================================")
print("INTELLIGENT OPTIMIZATION COMPLETE")
print("===================================")

print("Rows Generated:", len(result_df))

print("\nSample Output:\n")

print(

    result_df.sample(20)

)
