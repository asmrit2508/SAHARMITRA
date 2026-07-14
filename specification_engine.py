"""
=========================================================
SAHARMITRA PRODUCT SPECIFICATION ENGINE
=========================================================

Selects the most appropriate equipment specification
based on municipality characteristics.
"""

import re


def municipality_scale(population):

    if population < 100000:
        return "SMALL"

    elif population < 500000:
        return "MEDIUM"

    else:
        return "LARGE"


def get_specification(muni, equip):

    scale = municipality_scale(muni["population"])

    equipment = equip["equipment_name"].lower()

    flood = muni["flood_risk_index"]

    road = muni["road_network_km"]

    water = muni["water_supply_coverage_percent"]

    waste = muni["waste_generation_tpd"]


    # =====================================================
    # PUMPS
    # =====================================================

    if "pump" in equipment:

        if flood >= 8:

            return (
                "40 HP Industrial Pump",
                1.80
            )

        elif flood >= 5:

            return (
                "15 HP Municipal Pump",
                1.40
            )

        else:

            return (
                "5 HP Standard Pump",
                1.00
            )


    # =====================================================
    # TANKERS
    # =====================================================

    elif "tanker" in equipment:

        if scale == "LARGE":

            return (
                "10000 L Capacity",
                1.80
            )

        elif scale == "MEDIUM":

            return (
                "5000 L Capacity",
                1.35
            )

        else:

            return (
                "2000 L Capacity",
                1.00
            )


    # =====================================================
    # GARBAGE COMPACTORS
    # =====================================================

    elif "compactor" in equipment:

        if waste >= 200:

            return (
                "18 m³ Heavy Duty",
                1.75
            )

        elif waste >= 80:

            return (
                "10 m³ Standard",
                1.35
            )

        else:

            return (
                "5 m³ Compact",
                1.00
            )


    # =====================================================
    # CONTAINERS
    # =====================================================

    elif "container" in equipment or "bin" in equipment:

        if scale == "LARGE":

            return (
                "3000 L Container",
                1.50
            )

        elif scale == "MEDIUM":

            return (
                "1000 L Container",
                1.20
            )

        else:

            return (
                "500 L Container",
                1.00
            )


    # =====================================================
    # EXCAVATORS
    # =====================================================

    elif "excavator" in equipment:

        if road > 500:

            return (
                "Heavy Duty Excavator",
                1.80
            )

        elif road > 200:

            return (
                "Standard Excavator",
                1.35
            )

        else:

            return (
                "Mini Excavator",
                1.00
            )


    # =====================================================
    # ROAD ROLLERS
    # =====================================================

    elif "roller" in equipment:

        if scale == "LARGE":

            return (
                "14 Ton Roller",
                1.70
            )

        elif scale == "MEDIUM":

            return (
                "8 Ton Roller",
                1.30
            )

        else:

            return (
                "3 Ton Roller",
                1.00
            )


    # =====================================================
    # ROBOTS
    # =====================================================

    elif "robot" in equipment:

        if scale == "LARGE":

            return (
                "AI Enabled Robot",
                1.80
            )

        elif scale == "MEDIUM":

            return (
                "Semi Automatic Robot",
                1.35
            )

        else:

            return (
                "Basic Inspection Robot",
                1.00
            )


    # =====================================================
    # CAMERAS
    # =====================================================

    elif "camera" in equipment:

        if scale == "LARGE":

            return (
                "4K AI Camera System",
                1.60
            )

        elif scale == "MEDIUM":

            return (
                "HD Camera System",
                1.25
            )

        else:

            return (
                "Standard CCTV Unit",
                1.00
            )


    # =====================================================
    # GENERATORS
    # =====================================================

    elif "generator" in equipment:

        if scale == "LARGE":

            return (
                "100 KVA Generator",
                1.80
            )

        elif scale == "MEDIUM":

            return (
                "40 KVA Generator",
                1.35
            )

        else:

            return (
                "15 KVA Generator",
                1.00
            )


    # =====================================================
    # DRONES
    # =====================================================

    elif "drone" in equipment:

        if scale == "LARGE":

            return (
                "90 min Endurance Drone",
                1.70
            )

        elif scale == "MEDIUM":

            return (
                "45 min Endurance Drone",
                1.30
            )

        else:

            return (
                "20 min Endurance Drone",
                1.00
            )


    # =====================================================
    # DEFAULT
    # =====================================================

    return (
        "Standard Municipal Variant",
        1.00
    )
    