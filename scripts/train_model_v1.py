import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# ==========================================
# LOAD FILES
# ==========================================

municipality_df = pd.read_csv(
    "data/raw/municipality_master_v2.csv"
)

demand_df = pd.read_csv(
    "data/raw/municipality_equipment_demand.csv"
)

# ==========================================
# FILTER ONLY E001
# Garbage Compactor Truck
# ==========================================

demand_df = demand_df[
    demand_df["equipment_id"] == "E001"
]

print("\nRows Selected:", len(demand_df))

# ==========================================
# MERGE DATASETS
# ==========================================

df = pd.merge(

    demand_df,

    municipality_df,

    left_on="municipality",

    right_on="municipality_name"

)

# ==========================================
# INPUT FEATURES
# ==========================================

X = df[[

    "population",

    "area_sq_km",

    "road_network_km",

    "waste_generation_tpd",

    "flood_risk_index",

    "industrial_activity_index",

    "construction_activity_index",

    "tourism_activity_index"

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

    test_size=0.20,

    random_state=42

)

print("\nTraining Rows:", len(X_train))
print("Testing Rows:", len(X_test))

# ==========================================
# MODEL CREATION
# ==========================================

model = RandomForestRegressor(

    n_estimators=100,

    random_state=42

)

# ==========================================
# TRAIN MODEL
# ==========================================

print("\nTraining Model...\n")

model.fit(

    X_train,

    y_train

)

# ==========================================
# PREDICTION
# ==========================================

predictions = model.predict(

    X_test

)

# ==========================================
# EVALUATION METRICS
# ==========================================

# MAE

mae = mean_absolute_error(

    y_test,

    predictions

)

# RMSE

rmse = np.sqrt(

    mean_squared_error(

        y_test,

        predictions
    )
)

# R2 SCORE

r2 = r2_score(

    y_test,

    predictions

)

# ==========================================
# PRINT RESULTS
# ==========================================

print("\n====================================")
print("MODEL TRAINING COMPLETE")
print("====================================")

print("MAE Score :", round(mae,3))

print("RMSE Score :", round(rmse,3))

print("R2 Score :", round(r2,3))

# ==========================================
# ACTUAL VS PREDICTED
# ==========================================

print("\nActual vs Predicted:\n")

comparison = pd.DataFrame({

    "Actual Demand": y_test,

    "Predicted Demand":
        predictions.round(2)

})

print(

    comparison.head(10)

)

# ==========================================
# FEATURE IMPORTANCE
# ==========================================

print("\n====================================")
print("FEATURE IMPORTANCE")
print("====================================\n")

importance = pd.DataFrame({

    "Feature": X.columns,

    "Importance":
        model.feature_importances_

})

importance = importance.sort_values(

    by="Importance",

    ascending=False

)

print(

    importance

)

# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(

    model,

    "data/raw/garbage_truck_model.pkl"

)

print("\n====================================")
print("MODEL SAVED SUCCESSFULLY")
print("====================================")