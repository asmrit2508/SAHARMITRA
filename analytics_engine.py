# =========================================================
# SAHARMITRA ANALYTICS ENGINE
# =========================================================

"""
Purpose:
Generate analytics summaries from procurement recommendations.

Outputs:

1. Category Distribution
2. Priority Distribution
3. Procurement Route Distribution
4. Top Costly Equipment

This data will later be used inside app.py
for dashboard charts and visual insights.
"""

import pandas as pd


# =========================================================
# CATEGORY DISTRIBUTION
# =========================================================

def get_category_distribution(
    result_df
):

    category_summary = (
        result_df[
            "Category"
        ]
        .value_counts()
        .reset_index()
    )

    category_summary.columns = [

        "Category",

        "Count"

    ]

    return category_summary


# =========================================================
# PRIORITY DISTRIBUTION
# =========================================================

def get_priority_distribution(
    result_df
):

    priority_summary = (
        result_df[
            "Priority"
        ]
        .value_counts()
        .reset_index()
    )

    priority_summary.columns = [

        "Priority",

        "Count"

    ]

    return priority_summary


# =========================================================
# PROCUREMENT ROUTE DISTRIBUTION
# =========================================================

def get_procurement_route_distribution(
    result_df
):

    route_summary = (
        result_df[
            "Procurement Route"
        ]
        .value_counts()
        .reset_index()
    )

    route_summary.columns = [

        "Procurement Route",

        "Count"

    ]

    return route_summary


# =========================================================
# TOP COSTLY EQUIPMENT
# =========================================================

def get_top_cost_equipment(
    result_df,
    top_n=5
):

    top_cost_summary = (
        result_df
        .sort_values(
            by="Estimated Cost",
            ascending=False
        )
        .head(top_n)
    )

    return top_cost_summary


# =========================================================
# MASTER ANALYTICS FUNCTION
# =========================================================

def generate_procurement_analytics(
    result_df
):

    analytics = {

        "category_distribution":

            get_category_distribution(
                result_df
            ),

        "priority_distribution":

            get_priority_distribution(
                result_df
            ),

        "route_distribution":

            get_procurement_route_distribution(
                result_df
            ),

        "top_cost_equipment":

            get_top_cost_equipment(
                result_df
            )

    }

    return analytics


# =========================================================
# OPTIONAL TEST
# =========================================================

if __name__ == "__main__":

    sample_data = pd.DataFrame({

        "Equipment": [

            "Garbage Truck",

            "Road Roller",

            "Drainage Pump",

            "Excavator",

            "Water Tanker"

        ],

        "Category": [

            "Waste Management",

            "Road Maintenance",

            "Drainage",

            "Construction",

            "Water Supply"

        ],

        "Priority": [

            "HIGH",

            "MEDIUM",

            "HIGH",

            "LOW",

            "HIGH"

        ],

        "Estimated Cost": [

            40,

            25,

            18,

            55,

            22

        ],

        "Procurement Route": [

            "GeM Portal",

            "Open Tender",

            "GeM Portal",

            "Special Approval",

            "Limited Tender"

        ]

    })

    analytics_result = generate_procurement_analytics(
        sample_data
    )

    print("\n===== CATEGORY DISTRIBUTION =====\n")

    print(
        analytics_result[
            "category_distribution"
        ]
    )

    print("\n===== PRIORITY DISTRIBUTION =====\n")

    print(
        analytics_result[
            "priority_distribution"
        ]
    )

    print("\n===== ROUTE DISTRIBUTION =====\n")

    print(
        analytics_result[
            "route_distribution"
        ]
    )

    print("\n===== TOP COST EQUIPMENT =====\n")

    print(
        analytics_result[
            "top_cost_equipment"
        ]
    )
    