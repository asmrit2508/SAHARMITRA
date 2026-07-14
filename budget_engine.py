# =========================================================
# SAHARMITRA BUDGET FEASIBILITY ENGINE
# =========================================================

"""
Purpose:
Evaluate whether recommended procurement cost
fits inside municipality annual budget.

Inputs:
1. annual_budget_lakhs
2. procurement_cost_lakhs

Outputs:
1. Budget Utilization %
2. Remaining Budget
3. Budget Status
"""


# =========================================================
# MAIN BUDGET CALCULATOR
# =========================================================

def calculate_budget_feasibility(
    annual_budget_lakhs,
    procurement_cost_lakhs
):

    # ---------------------------------------------
    # BUDGET UTILIZATION %
    # ---------------------------------------------

    utilization_percent = round(
        (
            procurement_cost_lakhs /
            annual_budget_lakhs
        ) * 100,
        2
    )

    # ---------------------------------------------
    # REMAINING BUDGET
    # ---------------------------------------------

    remaining_budget = round(
        annual_budget_lakhs -
        procurement_cost_lakhs,
        2
    )

    # ---------------------------------------------
    # STATUS ENGINE
    # ---------------------------------------------

    if utilization_percent <= 70:

        budget_status = "SAFE"

        status_message = (
            "Procurement comfortably fits within budget."
        )

    elif utilization_percent <= 100:

        budget_status = "WARNING"

        status_message = (
            "Procurement is consuming a large portion of budget."
        )

    else:

        budget_status = "EXCEEDED"

        status_message = (
            "Recommended procurement exceeds available budget."
        )

    # ---------------------------------------------
    # RETURN RESULTS
    # ---------------------------------------------

    return {

        "annual_budget_lakhs":
            annual_budget_lakhs,

        "procurement_cost_lakhs":
            procurement_cost_lakhs,

        "budget_utilization_percent":
            utilization_percent,

        "remaining_budget_lakhs":
            remaining_budget,

        "budget_status":
            budget_status,

        "status_message":
            status_message

    }


# =========================================================
# OPTIONAL TEST RUN
# =========================================================

if __name__ == "__main__":

    sample_budget = 4000      # 40 Crores
    sample_procurement = 2800

    result = calculate_budget_feasibility(
        sample_budget,
        sample_procurement
    )

    print("\n===== BUDGET ANALYSIS =====\n")

    print(
        "Annual Budget:",
        result["annual_budget_lakhs"],
        "Lakhs"
    )

    print(
        "Procurement Cost:",
        result["procurement_cost_lakhs"],
        "Lakhs"
    )

    print(
        "Utilization:",
        result["budget_utilization_percent"],
        "%"
    )

    print(
        "Remaining Budget:",
        result["remaining_budget_lakhs"],
        "Lakhs"
    )

    print(
        "Status:",
        result["budget_status"]
    )

    print(
        "Message:",
        result["status_message"]
    )
    