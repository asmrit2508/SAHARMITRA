import pandas as pd

# ==========================================
# LOAD DATASETS
# ==========================================

municipality_df = pd.read_csv("data/raw/municipality_master_v2.csv")
equipment_df = pd.read_csv("data/raw/equipment_master_v2.csv")

# ==========================================
# NORMALIZATION VALUES
# (Used so Mumbai/Delhi don't generate absurd demand)
# ==========================================

max_population = municipality_df["population"].max()
max_waste = municipality_df["waste_generation_tpd"].max()
max_road = municipality_df["road_network_km"].max()

all_demands = []

# ==========================================
# DEMAND GENERATION ENGINE V2
# ==========================================

# Loop through every municipality
for _, municipality in municipality_df.iterrows():

    municipality_name = municipality["municipality_name"]

    # Loop through every equipment
    for _, equipment in equipment_df.iterrows():

        score = 0

        # ----------------------------------
        # NORMALIZED DEPENDENCY LOGIC
        # ----------------------------------

        # Population dependency
        if equipment["depends_population"] == 1:
            score += (
                municipality["population"] / max_population
            )

        # Waste generation dependency
        if equipment["depends_waste_generation"] == 1:
            score += (
                municipality["waste_generation_tpd"] / max_waste
            )

        # Road network dependency
        if equipment["depends_road_network"] == 1:
            score += (
                municipality["road_network_km"] / max_road
            )

        # Water supply dependency
        if equipment["depends_water_supply"] == 1:
            score += (
                municipality["water_supply_coverage_percent"] / 100
            )

        # Drainage dependency
        if equipment["depends_drainage"] == 1:
            score += (
                municipality["drainage_coverage_percent"] / 100
            )

        # Sewerage dependency
        if equipment["depends_sewerage"] == 1:
            score += (
                municipality["sewerage_coverage_percent"] / 100
            )

        # ----------------------------------
        # FINAL DEMAND CALCULATION
        # ----------------------------------

        predicted_demand = round(
            score *
            equipment["criticality_score"] *
            1.2
        )

        # Minimum demand safeguard
        if predicted_demand < 1 and score > 0:
            predicted_demand = 1

        # Maximum cap safeguard
        if predicted_demand > 20:
            predicted_demand = 20

        # Store results
        all_demands.append({

            "municipality": municipality_name,
            "equipment_id": equipment["equipment_id"],
            "equipment_name": equipment["equipment_name"],
            "predicted_demand": predicted_demand

        })

# ==========================================
# CREATE FINAL DATAFRAME
# ==========================================

demand_df = pd.DataFrame(all_demands)

# Save output
demand_df.to_csv(
    "data/raw/municipality_equipment_demand.csv",
    index=False
)

# ==========================================
# OUTPUT
# ==========================================

print("===================================")
print("DEMAND GENERATION V2 COMPLETED")
print("===================================")

print("Total Rows Generated:", len(demand_df))

print("\nRandom Sample Output:\n")

# Random sample so you see different cities
print(demand_df.sample(20))
