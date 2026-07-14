import pandas as pd
import joblib

# =====================================
# LOAD FILES
# =====================================

municipality_df = pd.read_csv(
    "data/raw/municipality_master_v2.csv"
)

equipment_df = pd.read_csv(
    "data/raw/equipment_master_v2.csv"
)

# Load models

need_model = joblib.load(
    "models/need_classifier.pkl"
)

quantity_model = joblib.load(
    "models/quantity_predictor.pkl"
)

# =====================================
# USER INPUT
# =====================================

municipality_name = input(

    "\nEnter Municipality Name: "

)

# get municipality row

muni = municipality_df[

    municipality_df["municipality_name"] == municipality_name

]

if len(muni) == 0:

    print("Municipality Not Found")

    exit()

muni = muni.iloc[0]

recommendations = []

print("\nGenerating Recommendations...\n")

# =====================================
# LOOP THROUGH EQUIPMENT
# =====================================

for _, equip in equipment_df.iterrows():

    # classifier features

    clf_features = [[

        muni["population"],
        muni["road_network_km"],
        muni["waste_generation_tpd"],
        muni["water_supply_coverage_percent"],
        muni["drainage_coverage_percent"],
        muni["sewerage_coverage_percent"],
        muni["flood_risk_index"],
        muni["industrial_activity_index"],
        muni["construction_activity_index"],
        muni["tourism_activity_index"],

        equip["depends_population"],
        equip["depends_waste_generation"],
        equip["depends_road_network"],
        equip["depends_water_supply"],
        equip["depends_drainage"],
        equip["depends_sewerage"],
        equip["depends_flood_risk"],
        equip["depends_industrial_activity"],
        equip["depends_construction_activity"],
        equip["depends_tourism_activity"]

    ]]

    # predict need

    is_needed = need_model.predict(

        clf_features

    )[0]

    quantity = 0

    # =====================================
    # IF NEEDED → PREDICT QUANTITY
    # =====================================

    if is_needed == 1:

        qty_features = [[

            muni["population"],
            muni["road_network_km"],
            muni["waste_generation_tpd"],
            muni["water_supply_coverage_percent"],
            muni["drainage_coverage_percent"],
            muni["sewerage_coverage_percent"],
            muni["flood_risk_index"],
            muni["industrial_activity_index"],
            muni["construction_activity_index"],
            muni["tourism_activity_index"],

            equip["unit_cost_lakhs"],
            equip["criticality_score"],
            equip["usage_frequency_score"],

            equip["depends_population"],
            equip["depends_waste_generation"],
            equip["depends_road_network"],
            equip["depends_water_supply"],
            equip["depends_drainage"],
            equip["depends_sewerage"],
            equip["depends_flood_risk"],
            equip["depends_industrial_activity"],
            equip["depends_construction_activity"],
            equip["depends_tourism_activity"]

        ]]

        quantity = quantity_model.predict(

            qty_features

        )[0]

        quantity = round(quantity)

    # save result

    recommendations.append({

        "equipment_name":
            equip["equipment_name"],

        "category":
            equip["procurement_category"],

        "needed":
            is_needed,

        "predicted_quantity":
            quantity

    })

# =====================================
# CREATE OUTPUT
# =====================================

result_df = pd.DataFrame(

    recommendations

)

# only needed equipment

result_df = result_df[

    result_df["needed"] == 1

]

result_df = result_df.sort_values(

    by="predicted_quantity",

    ascending=False

)

# =====================================
# PRINT
# =====================================

print("\n====================================")
print("RECOMMENDATION ENGINE OUTPUT")
print("====================================\n")

print(

    result_df.head(30)

)
