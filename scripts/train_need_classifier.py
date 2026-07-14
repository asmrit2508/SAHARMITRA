import pandas as pd
import os
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

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
# MERGE DATASETS
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
# FEATURE SELECTION
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

    # equipment dependency features

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

y = merged_df["is_needed"]

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

print("\nTRAINING CLASSIFICATION MODEL...\n")

model = RandomForestClassifier(

    n_estimators=100,

    random_state=42

)

model.fit(

    X_train,

    y_train

)

# =====================================
# PREDICTIONS
# =====================================

y_pred = model.predict(

    X_test

)

# =====================================
# EVALUATION
# =====================================

accuracy = accuracy_score(

    y_test,

    y_pred

)

print("\n====================================")
print("CLASSIFIER TRAINING COMPLETE")
print("====================================")

print("\nAccuracy Score:", round(accuracy,3))

print("\nClassification Report:\n")

print(

    classification_report(

        y_test,

        y_pred

    )

)

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

    "models/need_classifier.pkl"

)

print("\nModel Saved Successfully")
