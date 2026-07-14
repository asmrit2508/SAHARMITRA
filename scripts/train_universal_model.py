import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# ==========================================
# LOAD FILES
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

# ==========================================
# MERGE ALL DATA
# ==========================================

df = pd.merge(

    demand_df,

    municipality_df,

    left_on="municipality",

    right_on="municipality_name"

)

df = pd.merge(

    df,

    equipment_df,

    on="equipment_id"

)

print("Total Training Rows:", len(df))

# ==========================================
# FEATURES
# ==========================================

X = df[[

    # Municipality Features

    "population",

    "area_sq_km",

    "road_network_km",

    "waste_generation_tpd",

    "flood_risk_index",

    "industrial_activity_index",

    "construction_activity_index",

    "tourism_activity_index",

    # Equipment Features

    "criticality_score",

    "usage_frequency_score",

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

]]

# ==========================================
# TARGET
# ==========================================

y = df["predicted_demand"]

# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.2,

    random_state=42

)

# ==========================================
# MODEL
# ==========================================

model = RandomForestRegressor(

    n_estimators=120,

    random_state=42,

    n_jobs=-1

)

# TRAIN

print("\nTraining Universal Model...\n")

model.fit(

    X_train,

    y_train

)

# ==========================================
# PREDICT
# ==========================================

predictions = model.predict(

    X_test

)

# ==========================================
# EVALUATE
# ==========================================

mae = mean_absolute_error(

    y_test,

    predictions

)

print("\n====================================")
print("UNIVERSAL MODEL TRAINED")
print("====================================")

print("Mean Absolute Error:", round(mae,2))

comparison = pd.DataFrame({

    "Actual Demand": y_test,

    "Predicted Demand":
        predictions.round(2)

})

print("\nSample Predictions:\n")

print(comparison.head(20))

# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(

    model,

    "data/raw/universal_procurement_model.pkl"

)

print("\nUniversal Model Saved Successfully")