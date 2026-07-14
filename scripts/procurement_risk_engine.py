import pandas as pd


class ProcurementRiskEngine:

    def calculate_risk(self, vendor):

        score = 0

        # ----------------------------
        # Vendor Rating
        # ----------------------------

        if vendor["Rating"] < 4.5:
            score += 2
        elif vendor["Rating"] < 4.7:
            score += 1

        # ----------------------------
        # Vendor Score
        # ----------------------------

        if vendor["Vendor Score"] < 0.60:
            score += 2
        elif vendor["Vendor Score"] < 0.75:
            score += 1

        # ----------------------------
        # Delivery Time
        # ----------------------------

        if vendor["Delivery"] > 25:
            score += 2
        elif vendor["Delivery"] > 18:
            score += 1

        # ----------------------------
        # GeM Availability
        # ----------------------------

        if vendor["GeM"] == "No":
            score += 1

        # ----------------------------
        # Final Risk
        # ----------------------------

        if score <= 2:

            return "LOW", "Reliable procurement"

        elif score <= 4:

            return "MEDIUM", "Moderate procurement risk"

        else:

            return "HIGH", "Vendor requires careful monitoring"
        