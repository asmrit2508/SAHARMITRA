import pandas as pd


class BudgetOptimizer:

    def __init__(self, budget_crore):

        self.total_budget = budget_crore * 100  # Crore → Lakhs


    def optimize(self, recommendations_df):

        df = recommendations_df.copy()

        priority_order = {
            "HIGH": 1,
            "MEDIUM": 2,
            "LOW": 3
        }

        df["priority_rank"] = df["Priority"].map(priority_order)

        df = df.sort_values(
            by=["priority_rank", "Vendor Score"],
            ascending=[True, False]
        )

        budget_remaining = self.total_budget

        procurement_status = []

        allocated_cost = []

        for _, row in df.iterrows():

            cost = row["Estimated Cost"]

            if cost <= budget_remaining:

                procurement_status.append("Approved")
                allocated_cost.append(cost)

                budget_remaining -= cost

            else:

                procurement_status.append("Deferred")
                allocated_cost.append(0)

        df["Procurement Status"] = procurement_status
        df["Allocated Cost"] = allocated_cost

        summary = {

            "Total Budget (Lakhs)": self.total_budget,

            "Budget Used (Lakhs)": sum(allocated_cost),

            "Budget Remaining (Lakhs)": budget_remaining,

            "Approved Equipment":

                (df["Procurement Status"] == "Approved").sum(),

            "Deferred Equipment":

                (df["Procurement Status"] == "Deferred").sum()

        }

        return df, summary