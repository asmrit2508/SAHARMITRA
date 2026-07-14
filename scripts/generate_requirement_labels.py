import pandas as pd
import os
import random

# ======================================
# LOAD DATA
# ======================================

municipality_df = pd.read_csv(
    "data/raw/municipality_master_v2.csv"
)

equipment_df = pd.read_csv(
    "data/raw/equipment_master_v2.csv"
)

# create output folder if missing
os.makedirs(
    "data/processed",
    exist_ok=True
)

all_rows = []

# ======================================
# CATEGORY WEIGHTS
# ======================================

CATEGORY_WEIGHTS = {

    "SWM": 1.40,

    "Drainage": 1.35,

    "Sewerage": 1.30,

    "Water Supply": 1.25,

    "Road Infra": 1.20,

    "Sanitation": 1.15,

    "Electrical": 0.80,

    "Emergency": 0.90,

    "Specialized": 0.35

}

print("\nSTARTING REQUIREMENT GENERATION...\n")

# ======================================
# LOOP THROUGH MUNICIPALITIES
# ======================================

for _, muni in municipality_df.iterrows():

    municipality_name = muni["municipality_name"]

    # ----------------------------------
    # Municipality normalized factors
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
    # LOOP EQUIPMENT
    # ======================================

    for _, equip in equipment_df.iterrows():

        score = 0

        # ----------------------------------
        # dependency scoring
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
        # CATEGORY WEIGHTING
        # ======================================

        category = equip["procurement_category"]

        category_weight = CATEGORY_WEIGHTS.get(
            category,
            1.0
        )

        score = score * category_weight

        # ======================================
        # DETERMINE NEEDED / NOT NEEDED
        # ======================================

        if category == "Specialized":

            threshold = 18

        else:

            threshold = 12

        if score >= threshold:

            is_needed = 1

        else:

            is_needed = 0

        # ======================================
        # REALISTIC QUANTITY ESTIMATION FINAL
        # ======================================

        if is_needed == 1:

            # municipality scale factor
            population_scale = muni["population"] / 1000000

            # -----------------------------
            # HIGH COST EQUIPMENT
            # -----------------------------
            if equip["unit_cost_lakhs"] >= 40:

                # fire tender, crane, excavator etc
                base_quantity = random.randint(1, 3)

                if population_scale > 3:
                    base_quantity += 1

                required_quantity = base_quantity

            # -----------------------------
            # MEDIUM COST EQUIPMENT
            # -----------------------------
            elif equip["unit_cost_lakhs"] >= 15:

                # road cutters, fogging machines etc
                base_quantity = random.randint(2, 5)

                if population_scale > 2:
                    base_quantity += 1

                if score > 25:
                    base_quantity += 1

                required_quantity = base_quantity

            # -----------------------------
            # LOW COST EQUIPMENT
            # -----------------------------
            else:

                # bins, portable tools etc
                base_quantity = random.randint(4, 8)

                if population_scale > 2:
                    base_quantity += 2

                if score > 25:
                    base_quantity += 1

                required_quantity = base_quantity

            # safety cap
            if required_quantity > 12:
                required_quantity = 12

        else:

            required_quantity = 0

        # ======================================
        # SAVE ROW
        # ======================================

        all_rows.append({

            "municipality":
                municipality_name,

            "equipment_id":
                equip["equipment_id"],

            "equipment_name":
                equip["equipment_name"],

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
# CREATE FINAL DATAFRAME
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