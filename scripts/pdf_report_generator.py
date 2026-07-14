from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


class ProcurementPDFGenerator:

    def generate(
        self,
        municipality,
        result_df,
        budget_summary,
        filename
    ):

        doc = SimpleDocTemplate(filename)

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph(
                "<b><font size=18>SAHARMITRA</font></b>",
                styles["Title"]
            )
        )

        story.append(
            Paragraph(
                "AI Municipal Procurement Report",
                styles["Heading2"]
            )
        )

        story.append(Spacer(1,0.3*inch))

        story.append(
            Paragraph(
                f"<b>Municipality:</b> {municipality}",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1,0.2*inch))

        story.append(
            Paragraph(
                "<b>Budget Summary</b>",
                styles["Heading2"]
            )
        )

        summary_data = [

            ["Total Budget",
             budget_summary["Total Budget (Lakhs)"]],

            ["Budget Used",
             budget_summary["Budget Used (Lakhs)"]],

            ["Budget Remaining",
             budget_summary["Budget Remaining (Lakhs)"]],

            ["Approved",
             budget_summary["Approved Equipment"]],

            ["Deferred",
             budget_summary["Deferred Equipment"]]

        ]

        summary_table = Table(summary_data)

        summary_table.setStyle(

            TableStyle([

                ("GRID",(0,0),(-1,-1),1,colors.grey),

                ("BACKGROUND",(0,0),(-1,0),colors.lightblue),

                ("FONTNAME",(0,0),(-1,-1),"Helvetica"),

                ("BOTTOMPADDING",(0,0),(-1,-1),8)

            ])

        )

        story.append(summary_table)

        story.append(Spacer(1,0.3*inch))

        story.append(

            Paragraph(
                "<b>Top Procurement Recommendations</b>",
                styles["Heading2"]
            )

        )

        table_data = [[

            "Equipment",

            "Vendor",

            "Specification",

            "Qty",

            "Priority",

            "Cost"

        ]]

        for _, row in result_df.head(20).iterrows():

            table_data.append([

                row["Equipment"],

                row["Best Vendor"],

                row["Specification"],

                row["Quantity"],

                row["Priority"],

                row["Estimated Cost"]

            ])

        equipment_table = Table(table_data)

        equipment_table.setStyle(

            TableStyle([

                ("GRID",(0,0),(-1,-1),0.5,colors.grey),

                ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

                ("TEXTCOLOR",(0,0),(-1,0),colors.white),

                ("FONTNAME",(0,0),(-1,-1),"Helvetica"),

                ("BOTTOMPADDING",(0,0),(-1,-1),6)

            ])

        )

        story.append(equipment_table)

        doc.build(story)