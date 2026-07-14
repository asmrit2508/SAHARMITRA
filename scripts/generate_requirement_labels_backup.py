import pandas as pd
import os

# ======================================
# LOAD DATA
# ======================================

municipality_df = pd.read_csv(
    "data/raw/municipality_master_v2.csv"
)

equipment_df = pd.read_csv(
    "data/raw/equipment_master_v2.csv"
)

# Create output folder if missing
os.makedirs(
    "data/processed",
    exist_ok=True
)

all_rows = []

print("\nSTARTING REQUIREMENT GENERATION...\n")

# ======================================
# LOOP THROUGH MUNICIPALITIES
# ======================================

for _, muni in municipality_df.iterrows():

    municipality_name = muni["municipality_name"]

    # ----------------------------------
    # Normalize municipal attributes
    # ----------------------------------

    population_score = muni["population"] / 1000000
    waste_score = muni["waste_generation_tpd"] / 100
    road_score = muni["road_network_km"] / 100
    water_score = muni["water_supply_coverage_percent"] / 10
    drainage_score = muni["drainage_coverage_percent"] / 10
    sewerage_score = muni["sewerage_coverage_percent"] / 10
    flood_score = muni["flood_risk_index"]
    industrial_score = muni["industrial_activity_index"]
    construction_score = muni["construction_activity_index"]
    tourism_score = muni["tourism_activity_index"]

    # ======================================
    # LOOP THROUGH EQUIPMENT
    # ======================================

    for _, equip in equipment_df.iterrows():

        score = 0

        # ----------------------------------
        # Dependency based scoring
        # ----------------------------------

        if equip["depends_population"] == 1:
            score += population_score * 1.2

        if equip["depends_waste_generation"] == 1:
            score += waste_score * 1.5

        if equip["depends_road_network"] == 1:
            score += road_score * 1.3

        if equip["depends_water_supply"] == 1:
            score += water_score * 1.0

        if equip["depends_drainage"] == 1:
            score += drainage_score * 1.2

        if equip["depends_sewerage"] == 1:
            score += sewerage_score * 1.2

        if equip["depends_flood_risk"] == 1:
            score += flood_score * 1.5

        if equip["depends_industrial_activity"] == 1:
            score += industrial_score * 1.3

        if equip["depends_construction_activity"] == 1:
            score += construction_score * 1.1

        if equip["depends_tourism_activity"] == 1:
            score += tourism_score * 1.0

        # ======================================
        # DETERMINE NEEDED / NOT NEEDED
        # ======================================

        if score >= 12:
            is_needed = 1
        else:
            is_needed = 0

        # ======================================
        # REALISTIC QUANTITY ESTIMATION
        # ======================================

        if is_needed == 1:

            # Heavy / expensive equipment
            if equip["unit_cost_lakhs"] >= 40:

                if score < 20:
                    required_quantity = 1

                elif score < 35:
                    required_quantity = 2

                elif score < 50:
                    required_quantity = 3

                else:
                    required_quantity = 4

            # Medium cost equipment
            elif equip["unit_cost_lakhs"] >= 15:

                if score < 20:
                    required_quantity = 2

                elif score < 35:
                    required_quantity = 4

                elif score < 50:
                    required_quantity = 6

                else:
                    required_quantity = 8

            # Low cost operational equipment
            else:

                if score < 20:
                    required_quantity = 3

                elif score < 35:
                    required_quantity = 6

                elif score < 50:
                    required_quantity = 10

                else:
                    required_quantity = 15

        else:

            required_quantity = 0

        # ======================================
        # SAVE ROW
        # ======================================

        all_rows.append({

            "municipality": municipality_name,

            "equipment_id": equip["equipment_id"],

            "equipment_name": equip["equipment_name"],

            "procurement_category":
                equip["procurement_category"],

            "requirement_score":
                round(score, 2),

            "is_needed":
                is_needed,

            "required_quantity":
                required_quantity

        })

# ======================================
# CREATE DATAFRAME
# ======================================

final_df = pd.DataFrame(
    all_rows
)

# ======================================
# SAVE CSV
# ======================================

final_df.to_csv(
    "data/processed/equipment_requirement_dataset.csv",
    index=False
)

# ======================================
# SUMMARY
# ======================================

print("\n===================================")
print("REQUIREMENT GENERATION COMPLETE")
print("===================================")

print("Rows Generated:", len(final_df))

print("\nRandom Sample:\n")

print(
    final_df.sample(20)
)
