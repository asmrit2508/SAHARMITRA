import pandas as pd
import os
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

# =====================================
# LOAD FILES
# =====================================

municipality_df = pd.read_csv(
    "data/raw/municipality_master_v2.csv"
)

equipment_df = pd.read_csv(
    "data/raw/equipment_master_v2.csv"
)

requirement_df = pd.read_csv(
    "data/processed/equipment_requirement_dataset.csv"
)

# =====================================
# KEEP ONLY NEEDED EQUIPMENT
# =====================================

requirement_df = requirement_df[
    requirement_df["is_needed"] == 1
]

# =====================================
# MERGE
# =====================================

merged_df = requirement_df.merge(

    municipality_df,

    left_on="municipality",

    right_on="municipality_name"

)

merged_df = merged_df.merge(

    equipment_df,

    on="equipment_id"

)

# =====================================
# FEATURES
# =====================================

features = [

    # municipality features

    "population",
    "road_network_km",
    "waste_generation_tpd",
    "water_supply_coverage_percent",
    "drainage_coverage_percent",
    "sewerage_coverage_percent",
    "flood_risk_index",
    "industrial_activity_index",
    "construction_activity_index",
    "tourism_activity_index",

    # equipment features

    "unit_cost_lakhs",
    "criticality_score",
    "usage_frequency_score",

    # dependencies

    "depends_population",
    "depends_waste_generation",
    "depends_road_network",
    "depends_water_supply",
    "depends_drainage",
    "depends_sewerage",
    "depends_flood_risk",
    "depends_industrial_activity",
    "depends_construction_activity",
    "depends_tourism_activity"

]

X = merged_df[features]

y = merged_df["required_quantity"]

# =====================================
# TRAIN TEST SPLIT
# =====================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42

)

# =====================================
# TRAIN MODEL
# =====================================

print("\nTRAINING QUANTITY MODEL...\n")

model = RandomForestRegressor(

    n_estimators=100,

    random_state=42

)

model.fit(

    X_train,

    y_train

)

# =====================================
# PREDICTION
# =====================================

y_pred = model.predict(

    X_test
)

# =====================================
# EVALUATION
# =====================================

mae = mean_absolute_error(

    y_test,
    y_pred

)

rmse = mean_squared_error(

    y_test,
    y_pred

) ** 0.5

r2 = r2_score(

    y_test,
    y_pred

)

print("\n====================================")
print("QUANTITY MODEL COMPLETE")
print("====================================")

print("\nMAE Score :", round(mae,3))
print("RMSE Score:", round(rmse,3))
print("R2 Score  :", round(r2,3))

# =====================================
# SAMPLE OUTPUT
# =====================================

sample_df = pd.DataFrame({

    "Actual Quantity": y_test.values[:10],

    "Predicted Quantity": y_pred[:10]

})

print("\nActual vs Predicted:\n")

print(sample_df)

# =====================================
# FEATURE IMPORTANCE
# =====================================

importance_df = pd.DataFrame({

    "Feature": features,

    "Importance": model.feature_importances_

})

importance_df = importance_df.sort_values(

    by="Importance",

    ascending=False

)

print("\n====================================")
print("FEATURE IMPORTANCE")
print("====================================\n")

print(

    importance_df.head(10)

)

# =====================================
# SAVE MODEL
# =====================================

os.makedirs(

    "models",

    exist_ok=True

)

joblib.dump(

    model,

    "models/quantity_predictor.pkl"

)

print("\nModel Saved Successfully")