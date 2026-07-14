import pandas as pd


class VendorSelectionEngine:

    def __init__(self, vendor_database):

        self.vendor_df = pd.read_csv(vendor_database)

    # ----------------------------------------------------
    # NORMALIZATION
    # ----------------------------------------------------

    def normalize(self, series, reverse=False):

        if reverse:

            return (
                series.max() - series
            ) / (
                series.max() - series.min() + 1e-6
            )

        return (
            series - series.min()
        ) / (
            series.max() - series.min() + 1e-6
        )

    # ----------------------------------------------------
    # BEST VENDOR
    # ----------------------------------------------------

    def get_best_vendor(self, equipment_id):

        vendors = self.vendor_df[
            self.vendor_df["equipment_id"] == equipment_id
        ].copy()

        if vendors.empty:

            return None

        vendors["price_score"] = self.normalize(
            vendors["quoted_price_lakhs"],
            reverse=True
        )

        vendors["quality_score_norm"] = self.normalize(
            vendors["quality_score"]
        )

        vendors["delivery_score"] = self.normalize(
            vendors["delivery_days"],
            reverse=True
        )

        vendors["rating_score"] = self.normalize(
            vendors["vendor_rating"]
        )

        vendors["warranty_score"] = self.normalize(
            vendors["warranty_years"]
        )

        vendors["gem_score"] = vendors[
            "gem_available"
        ].map({
            "Yes": 1,
            "No": 0
        })

        # -----------------------------------------
        # FINAL PROCUREMENT SCORE
        # -----------------------------------------

        vendors["vendor_score"] = (

            0.35 * vendors["price_score"]

            +

            0.25 * vendors["quality_score_norm"]

            +

            0.15 * vendors["rating_score"]

            +

            0.10 * vendors["delivery_score"]

            +

            0.10 * vendors["warranty_score"]

            +

            0.05 * vendors["gem_score"]

        )

        best = vendors.sort_values(

            by="vendor_score",

            ascending=False

        ).iloc[0]

        return {

            "Vendor":

                best["vendor_name"],

            "Specification":

                best["specification"],

            "Price":

                best["quoted_price_lakhs"],

            "Quality":

                best["quality_score"],

            "Rating":

                best["vendor_rating"],

            "Warranty":

                best["warranty_years"],

            "Delivery":

                best["delivery_days"],

            "GeM":

                best["gem_available"],

            "Vendor Score":

                round(best["vendor_score"], 3)

        }