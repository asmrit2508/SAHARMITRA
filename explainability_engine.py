# =========================================================
# SAHARMITRA EXPLAINABILITY ENGINE
# =========================================================

"""
Purpose:
Explain WHY a particular equipment was recommended.

This engine checks municipal parameters
and equipment dependency flags and generates
human-readable explanations.

Example:

Garbage Truck recommended because:

- High waste generation
- Large population
- High industrial activity
"""


# =========================================================
# MAIN EXPLANATION FUNCTION
# =========================================================

def generate_explanation(
    municipality_data,
    equipment_data
):

    reasons = []

    # ---------------------------------------------
    # POPULATION CHECK
    # ---------------------------------------------

    if (
        equipment_data["depends_population"] == 1
        and municipality_data["population"] > 300000
    ):

        reasons.append(
            "High population increases service demand."
        )

    # ---------------------------------------------
    # WASTE GENERATION CHECK
    # ---------------------------------------------

    if (
        equipment_data["depends_waste_generation"] == 1
        and municipality_data["waste_generation_tpd"] > 100
    ):

        reasons.append(
            "High waste generation requires waste management equipment."
        )

    # ---------------------------------------------
    # ROAD NETWORK CHECK
    # ---------------------------------------------

    if (
        equipment_data["depends_road_network"] == 1
        and municipality_data["road_network_km"] > 120
    ):

        reasons.append(
            "Large road network increases infrastructure maintenance demand."
        )

    # ---------------------------------------------
    # WATER SUPPLY CHECK
    # ---------------------------------------------

    if (
        equipment_data["depends_water_supply"] == 1
        and municipality_data["water_supply_coverage_percent"] < 75
    ):

        reasons.append(
            "Low water supply coverage indicates infrastructure requirement."
        )

    # ---------------------------------------------
    # DRAINAGE CHECK
    # ---------------------------------------------

    if (
        equipment_data["depends_drainage"] == 1
        and municipality_data["drainage_coverage_percent"] < 70
    ):

        reasons.append(
            "Low drainage coverage requires drainage infrastructure support."
        )

    # ---------------------------------------------
    # SEWERAGE CHECK
    # ---------------------------------------------

    if (
        equipment_data["depends_sewerage"] == 1
        and municipality_data["sewerage_coverage_percent"] < 70
    ):

        reasons.append(
            "Low sewerage coverage increases sanitation infrastructure demand."
        )

    # ---------------------------------------------
    # FLOOD RISK CHECK
    # ---------------------------------------------

    if (
        equipment_data["depends_flood_risk"] == 1
        and municipality_data["flood_risk_index"] >= 7
    ):

        reasons.append(
            "High flood risk requires emergency and drainage equipment."
        )

    # ---------------------------------------------
    # INDUSTRIAL ACTIVITY CHECK
    # ---------------------------------------------

    if (
        equipment_data["depends_industrial_activity"] == 1
        and municipality_data["industrial_activity_index"] >= 7
    ):

        reasons.append(
            "High industrial activity increases municipal equipment demand."
        )

    # ---------------------------------------------
    # CONSTRUCTION ACTIVITY CHECK
    # ---------------------------------------------

    if (
        equipment_data["depends_construction_activity"] == 1
        and municipality_data["construction_activity_index"] >= 7
    ):

        reasons.append(
            "High construction activity requires infrastructure support equipment."
        )

    # ---------------------------------------------
    # TOURISM ACTIVITY CHECK
    # ---------------------------------------------

    if (
        equipment_data["depends_tourism_activity"] == 1
        and municipality_data["tourism_activity_index"] >= 7
    ):

        reasons.append(
            "High tourism activity increases public infrastructure demand."
        )

    # ---------------------------------------------
    # DEFAULT EXPLANATION
    # ---------------------------------------------

    if len(reasons) == 0:

        reasons.append(
            "General municipal operational requirement detected."
        )

    # ---------------------------------------------
    # RETURN RESULT
    # ---------------------------------------------

    return reasons


# =========================================================
# OPTIONAL TEST
# =========================================================

if __name__ == "__main__":

    sample_municipality = {

        "population": 500000,
        "waste_generation_tpd": 250,
        "road_network_km": 180,
        "water_supply_coverage_percent": 60,
        "drainage_coverage_percent": 55,
        "sewerage_coverage_percent": 62,
        "flood_risk_index": 8,
        "industrial_activity_index": 7,
        "construction_activity_index": 6,
        "tourism_activity_index": 5

    }

    sample_equipment = {

        "depends_population": 1,
        "depends_waste_generation": 1,
        "depends_road_network": 0,
        "depends_water_supply": 0,
        "depends_drainage": 0,
        "depends_sewerage": 0,
        "depends_flood_risk": 0,
        "depends_industrial_activity": 1,
        "depends_construction_activity": 0,
        "depends_tourism_activity": 0

    }

    result = generate_explanation(
        sample_municipality,
        sample_equipment
    )

    print("\n===== EXPLANATION ENGINE =====\n")

    for reason in result:

        print("-", reason)
        