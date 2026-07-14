import pandas as pd

# ============================================
# LOAD FILES
# ============================================

allocation_df = pd.read_csv(
    "data/raw/optimized_allocation_v4.csv"
)

equipment_df = pd.read_csv(
    "data/raw/equipment_master_v2.csv"
)

municipality_df = pd.read_csv(
    "data/raw/municipality_master_v2.csv"
)

results = []

print("\nSTARTING PROCUREMENT ANALYSIS...\n")

# ============================================
# PROCESS EACH ROW
# ============================================

for _, row in allocation_df.iterrows():

    municipality = row["municipality"]

    equipment_id = row["equipment_id"]

    demand = row["demand"]

    allocated = row["allocated"]

    equipment_name = row["equipment_name"]

    # -------------------------
    # PROCUREMENT GAP
    # -------------------------

    procurement_needed = demand - allocated

    if procurement_needed < 0:
        procurement_needed = 0

    # -------------------------
    # GAP PERCENTAGE
    # -------------------------

    if demand == 0:
        gap_percent = 0
    else:
        gap_percent = (
            procurement_needed / demand
        ) * 100

    # -------------------------
    # URGENCY
    # -------------------------

    if gap_percent > 70:
        urgency = "HIGH"

    elif gap_percent >= 40:
        urgency = "MEDIUM"

    else:
        urgency = "LOW"

    # -------------------------
    # EQUIPMENT COST
    # -------------------------

    equipment_row = equipment_df[
        equipment_df["equipment_id"]
        == equipment_id
    ]

    unit_cost = equipment_row[
        "unit_cost_lakhs"
    ].values[0]

    procurement_cost = (
        procurement_needed * unit_cost
    )

    # -------------------------
    # MUNICIPALITY BUDGET
    # -------------------------

    municipality_row = municipality_df[
        municipality_df["municipality_name"]
        == municipality
    ]

    annual_budget = municipality_row[
        "annual_budget_lakhs"
    ].values[0]

    # -------------------------
    # BUDGET CHECK
    # -------------------------

    budget_limit = annual_budget * 0.15

    if procurement_cost > budget_limit:
        feasible = "NO"

    else:
        feasible = "YES"

    # -------------------------
    # STORE RESULTS
    # -------------------------

    results.append({

        "municipality": municipality,

        "equipment_id": equipment_id,

        "equipment_name": equipment_name,

        "predicted_demand": demand,

        "allocated_stock": allocated,

        "procurement_needed":
            procurement_needed,

        "urgency_level":
            urgency,

        "unit_cost_lakhs":
            unit_cost,

        "estimated_procurement_cost":
            procurement_cost,

        "annual_budget_lakhs":
            annual_budget,

        "budget_feasible":
            feasible

    })

# ============================================
# SAVE CSV
# ============================================

result_df = pd.DataFrame(results)

result_df.to_csv(

    "data/raw/procurement_recommendation.csv",

    index=False

)

# ============================================
# SUMMARY
# ============================================

print("\n==================================")
print("PROCUREMENT ANALYSIS COMPLETE")
print("==================================")

print("Rows Generated:",
      len(result_df))

print("\nSample Output:\n")

print(

    result_df.sample(20)

)