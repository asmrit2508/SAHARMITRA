import streamlit as st
import pandas as pd
import joblib
import io

from datetime import datetime
# from scripts.pdf_report_generator import ProcurementPDFGenerator
from scripts.procurement_risk_engine import ProcurementRiskEngine
from scripts.budget_optimizer import BudgetOptimizer
from scripts.procurement_engine import recommend_best_vendor
from models.vendor_engine import VendorSelectionEngine
from specification_engine import get_specification
from budget_engine import calculate_budget_feasibility
from explainability_engine import generate_explanation
from analytics_engine import generate_procurement_analytics
# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="शहरMitra",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

/* GLOBAL */

.main {
    background-color: #EEF2F7;
}

.block-container {
    padding-top: 1rem;
    max-width: 95%;
}



section[data-testid="stSidebar"] {

    background: linear-gradient(
        180deg,
        #061826 0%,
        #0B2447 55%,
        #19376D 100%
    );

    border-right: 1px solid #355C7D;
}
/* Make sidebar text visible */

section[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

/* Fix selectbox label */

[data-testid="stSidebar"] label {
    color: #F8FAFC !important;
    font-weight: 600 !important;
}

/* Keep dropdown selected value dark */

[data-baseweb="select"] div {
    color: #111827 !important;
}

/* DO NOT FORCE ALL TEXT WHITE */

/* HEADER */

.main-header {

    background: linear-gradient(
        135deg,
        #0B2447 0%,
        #19376D 55%,
        #576CBC 100%
    );

    padding: 30px;

    border-radius: 18px;

    box-shadow:
        0px 8px 20px rgba(0,0,0,0.15);

    margin-bottom: 28px;
}
.main-title {

    color: white;

    font-size: 42px;

    font-weight: 800;

    font-family: Arial;

    letter-spacing: 0.5px;
}
.main-subtitle {

    color: #D6E4FF;

    font-size: 17px;

    margin-top: 8px;

    font-weight: 500;

    line-height: 1.5;
}

/* SECTION */

.section-title {

    color: #FF2D2D;

    font-size: 26px;

    font-weight: 800;

    margin-top: 16px;

    margin-bottom: 18px;

    font-family: Arial;
}

/* CARDS */

.metric-card {

    background: linear-gradient(
        180deg,
        #FFFFFF 0%,
        #F8FAFC 100%
    );

    padding: 22px;

    border-radius: 16px;

    box-shadow:
        0px 4px 15px rgba(0,0,0,0.08);

    border-left: 6px solid #00B8A9;

    margin-bottom: 14px;

    transition: 0.3s ease;
}

.metric-label {
    color: #64748B;
    font-size: 14px;
    font-weight: 600;
}

.metric-value {
    color: #0F172A;
    font-size: 22px;
    font-weight: 700;
    margin-top: 4px;
}

/* INSIGHT CARD */

.insight-card {

    background: white;

    padding: 18px;

    border-radius: 14px;

    border: 1px solid #E2E8F0;

    box-shadow:
        0px 3px 10px rgba(0,0,0,0.05);

    text-align: center;

    margin-bottom: 12px;
}

.insight-title {
    color: #64748B;
    font-size: 13px;
}

.insight-value {
    color: #0F172A;
    font-size: 18px;
    font-weight: 700;
    margin-top: 5px;
}

/* BUTTON */

.stButton > button {

    width: 100%;

    background: linear-gradient(
        90deg,
        #00B8A9 0%,
        #14B8A6 100%
    );

    color: white;

    border: none;

    padding: 14px;

    font-weight: 700;

    border-radius: 12px;

    box-shadow:
        0px 4px 10px rgba(0,184,169,0.3);

    transition: 0.3s ease;
}
.stButton > button:hover {

    transform: translateY(-2px);

    background: #019B90;

    color: white;
}

/* DATAFRAME */

[data-testid="stDataFrame"] {
    border: 1px solid #E5E7EB;
    border-radius: 10px;
}

/* FOOTER */

.footer {
    text-align:center;
    color:#64748B;
    margin-top:40px;
    padding:20px;
}
/* MAKE ALL HEADINGS RED */


</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD FILES
# =========================================================

municipality_df = pd.read_csv(
    "data/raw/municipality_master_v2.csv"
)

equipment_df = pd.read_csv(
    "data/raw/equipment_master_v2.csv"
)

need_model = joblib.load(
    "models/need_classifier.pkl"
)

quantity_model = joblib.load(
    "models/quantity_predictor.pkl"
)

vendor_engine = VendorSelectionEngine(
    "data/raw/vendor_database.csv"
)
risk_engine = ProcurementRiskEngine()
# pdf_generator = ProcurementPDFGenerator()
#st.write(vendor_engine.vendor_df.head(10))
# =========================================================
# SIDEBAR (SIMPLIFIED)
# =========================================================

st.sidebar.title("🏛️ शहरMitra")
st.sidebar.markdown("---")

budget_crore = st.sidebar.slider(
    "Municipality Budget (₹ Crore)",
    min_value=10,
    max_value=5000,
    value=100,
    step=10
)
st.sidebar.markdown("Municipal Procurement Intelligence System")

st.sidebar.markdown("---")

municipality_names = municipality_df[
    "municipality_name"
].tolist()

selected_municipality = st.sidebar.selectbox(
    "Select Municipality",
    municipality_names
)

generate_button = st.sidebar.button(
    "Generate Procurement Analysis"
)

st.sidebar.markdown("---")

st.sidebar.caption("Internship Prototype")

# =========================================================
# HEADER
# =========================================================

st.markdown("""

<div class="main-header">

<div class="main-title">

शहरMitra

</div>

<div class="main-subtitle">

AI Powered Municipal Procurement & Infrastructure Intelligence Platform

</div>

</div>

""", unsafe_allow_html=True)

# =========================================================
# MUNICIPALITY DATA
# =========================================================

muni = municipality_df[
    municipality_df["municipality_name"]
    == selected_municipality
].iloc[0]

# =========================================================
# COMMON MUNICIPAL INDICATORS
# =========================================================

road_needing_repair = round(
    muni["road_network_km"] *
    (100 - muni["paved_road_percent"]) / 100
)

waste_processing_gap = max(
    0,
    muni["waste_generation_tpd"] -
    muni["solid_waste_processing_capacity_tpd"]
)

# =========================================================
# MUNICIPALITY OVERVIEW
# =========================================================

st.markdown(
    '<div class="section-title">Municipality Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-label">Population</div>
    <div class="metric-value">{int(muni["population"]):,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-label">Municipal Area</div>
    <div class="metric-value">{muni["area_sq_km"]} sq km</div>
    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-label">Administrative Wards</div>
    <div class="metric-value">{muni["wards"]}</div>
    </div>
    """, unsafe_allow_html=True)
with col4:

    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-label">Road Network</div>
    <div class="metric-value">{muni["road_network_km"]} KM</div>
    </div>
    """, unsafe_allow_html=True)
    
# =========================================================
# MUNICIPAL PROCUREMENT READINESS SCORE
# =========================================================

st.markdown(
    '<div class="section-title">Municipal Procurement Readiness</div>',
    unsafe_allow_html=True
)

readiness_score = (

    muni["water_supply_coverage_percent"] * 0.25 +

    muni["drainage_coverage_percent"] * 0.20 +

    muni["sewerage_coverage_percent"] * 0.20 +

    min(
        100,
        muni["solid_waste_processing_capacity_tpd"]
        /
        muni["waste_generation_tpd"]
        *100
    ) *0.20 +

    (10 - muni["flood_risk_index"]) *10 *0.15

)

readiness_score = round(readiness_score,1)

if readiness_score >= 85:

    grade = "A+"

    status = "Excellent"

elif readiness_score >= 70:

    grade = "A"

    status = "Good"

elif readiness_score >= 55:

    grade = "B"

    status = "Moderate"

else:

    grade = "C"

    status = "Needs Improvement"

col1,col2,col3 = st.columns(3)

with col1:

    st.metric(
        "Readiness Score",
        f"{readiness_score}/100"
    )

with col2:

    st.metric(
        "Grade",
        grade
    )

with col3:

    st.metric(
        "Status",
        status
    )

# =========================================================
# EXECUTIVE SUMMARY
# =========================================================

st.markdown(
    '<div class="section-title">Executive Summary</div>',
    unsafe_allow_html=True
)

summary = []

summary.append(
    f"Municipality Procurement Readiness is **{status} ({readiness_score}/100)**."
)

if waste_processing_gap > 0:

    summary.append(
        f"Solid waste processing deficit of **{waste_processing_gap} TPD** identified."
    )

if muni["flood_risk_index"] >= 7:

    summary.append(
        "High flood risk observed; flood mitigation equipment has been prioritised."
    )

if muni["water_supply_coverage_percent"] >= 95:

    summary.append(
        "Water supply coverage exceeds **95%**, indicating strong service availability."
    )

if road_needing_repair > 50:

    summary.append(
        f"Approximately **{road_needing_repair} km** of roads require improvement."
    )

summary.append(
    f"Municipality has **{muni['wards']} wards** serving approximately **{muni['population']:,}** citizens."
)

for item in summary:

    st.success(item)

# =========================================================
# PROCUREMENT JUSTIFICATION
# =========================================================

st.markdown(
    '<div class="section-title">Procurement Justification</div>',
    unsafe_allow_html=True
)

justification = []

if muni["waste_generation_tpd"] > 1000:
    justification.append(
        f"• High municipal solid waste generation ({muni['waste_generation_tpd']} TPD) requiring additional SWM equipment."
    )

if waste_processing_gap > 0:
    justification.append(
        f"• Existing waste processing capacity is insufficient by {waste_processing_gap} TPD."
    )

if road_needing_repair > 50:
    justification.append(
        f"• Approximately {road_needing_repair} km of roads require maintenance and repair."
    )

if muni["flood_risk_index"] >= 7:
    justification.append(
        "• High flood risk indicates need for drainage and emergency response equipment."
    )

if muni["population"] > 1000000:
    justification.append(
        f"• Large urban population ({muni['population']:,}) increases infrastructure demand."
    )



st.info("\n\n".join(justification))



# =========================================================
# INFRASTRUCTURE INSIGHTS
# =========================================================

st.markdown(
    '<div class="section-title">Municipal Service Coverage</div>',
    unsafe_allow_html=True
)

r1c1, r1c2, r1c3, r1c4 = st.columns(4)

with r1c1:

    st.markdown(f"""
    <div class="insight-card">
    <div class="insight-title">Water Supply</div>
    <div class="insight-value">{muni["water_supply_coverage_percent"]}%</div>
    </div>
    """, unsafe_allow_html=True)

with r1c2:

    st.markdown(f"""
    <div class="insight-card">
    <div class="insight-title">Drainage</div>
    <div class="insight-value">{muni["drainage_coverage_percent"]}%</div>
    </div>
    """, unsafe_allow_html=True)

with r1c3:

    st.markdown(f"""
    <div class="insight-card">
    <div class="insight-title">Sewerage</div>
    <div class="insight-value">{muni["sewerage_coverage_percent"]}%</div>
    </div>
    """, unsafe_allow_html=True)

with r1c4:

    st.markdown(f"""
    <div class="insight-card">
    <div class="insight-title">Flood Risk</div>
    <div class="insight-value">{muni["flood_risk_index"]}</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# SECOND INSIGHT ROW
# =========================================================

r2c1, r2c2, r2c3, r2c4 = st.columns(4)

with r2c1:

    st.markdown(f"""
    <div class="insight-card">
    <div class="insight-title">Industrial Activity</div>
    <div class="insight-value">{muni["industrial_activity_index"]}</div>
    </div>
    """, unsafe_allow_html=True)

with r2c2:

    st.markdown(f"""
    <div class="insight-card">
    <div class="insight-title">Construction Activity</div>
    <div class="insight-value">{muni["construction_activity_index"]}</div>
    </div>
    """, unsafe_allow_html=True)

with r2c3:

    st.markdown(f"""
    <div class="insight-card">
    <div class="insight-title">Tourism Activity</div>
    <div class="insight-value">{muni["tourism_activity_index"]}</div>
    </div>
    """, unsafe_allow_html=True)

with r2c4:

    st.markdown(f"""
    <div class="insight-card">
    <div class="insight-title">Municipality Class</div>
    <div class="insight-value">{muni["municipality_class"]}</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# RECOMMENDATION ENGINE
# =========================================================

if generate_button:

    recommendations = []

    total_estimated_cost = 0

    for _, equip in equipment_df.iterrows():

        # ------------------------------
        # NEED CLASSIFIER
        # ------------------------------

        classifier_features = pd.DataFrame([{

            "population":
                muni["population"],

            "road_network_km":
                muni["road_network_km"],

            "waste_generation_tpd":
                muni["waste_generation_tpd"],

            "water_supply_coverage_percent":
                muni["water_supply_coverage_percent"],

            "drainage_coverage_percent":
                muni["drainage_coverage_percent"],

            "sewerage_coverage_percent":
                muni["sewerage_coverage_percent"],

            "flood_risk_index":
                muni["flood_risk_index"],

            "industrial_activity_index":
                muni["industrial_activity_index"],

            "construction_activity_index":
                muni["construction_activity_index"],

            "tourism_activity_index":
                muni["tourism_activity_index"],

            "depends_population":
                equip["depends_population"],

            "depends_waste_generation":
                equip["depends_waste_generation"],

            "depends_road_network":
                equip["depends_road_network"],

            "depends_water_supply":
                equip["depends_water_supply"],

            "depends_drainage":
                equip["depends_drainage"],

            "depends_sewerage":
                equip["depends_sewerage"],

            "depends_flood_risk":
                equip["depends_flood_risk"],

            "depends_industrial_activity":
                equip["depends_industrial_activity"],

            "depends_construction_activity":
                equip["depends_construction_activity"],

            "depends_tourism_activity":
                equip["depends_tourism_activity"]

        }])

        need_prediction = need_model.predict(
            classifier_features
        )[0]

        # ------------------------------
        # QUANTITY MODEL
        # ------------------------------

        if need_prediction == 1:

            quantity_features = pd.DataFrame([{

                "population":
                    muni["population"],

                "road_network_km":
                    muni["road_network_km"],

                "waste_generation_tpd":
                    muni["waste_generation_tpd"],

                "water_supply_coverage_percent":
                    muni["water_supply_coverage_percent"],

                "drainage_coverage_percent":
                    muni["drainage_coverage_percent"],

                "sewerage_coverage_percent":
                    muni["sewerage_coverage_percent"],

                "flood_risk_index":
                    muni["flood_risk_index"],

                "industrial_activity_index":
                    muni["industrial_activity_index"],

                "construction_activity_index":
                    muni["construction_activity_index"],

                "tourism_activity_index":
                    muni["tourism_activity_index"],

                "unit_cost_lakhs":
                    equip["unit_cost_lakhs"],

                "criticality_score":
                    equip["criticality_score"],

                "usage_frequency_score":
                    equip["usage_frequency_score"],

                "depends_population":
                    equip["depends_population"],

                "depends_waste_generation":
                    equip["depends_waste_generation"],

                "depends_road_network":
                    equip["depends_road_network"],

                "depends_water_supply":
                    equip["depends_water_supply"],

                "depends_drainage":
                    equip["depends_drainage"],

                "depends_sewerage":
                    equip["depends_sewerage"],

                "depends_flood_risk":
                    equip["depends_flood_risk"],

                "depends_industrial_activity":
                    equip["depends_industrial_activity"],

                "depends_construction_activity":
                    equip["depends_construction_activity"],

                "depends_tourism_activity":
                    equip["depends_tourism_activity"]

            }])

            quantity_prediction = round(
                quantity_model.predict(
                    quantity_features
                )[0]
            )
            
            # -----------------------------------------
            # PRODUCT SPECIFICATION ENGINE
            # -----------------------------------------

            specification, specification_multiplier = get_specification(
                muni,
                equip
            )

            # ------------------------------
            # PRIORITY LOGIC
            # ------------------------------

            if quantity_prediction >= 8:
                priority = "HIGH"

            elif quantity_prediction >= 5:
                priority = "MEDIUM"

            else:
                priority = "LOW"


            # -----------------------------------------
            # COST CALCULATION (THIS WAS MISSING)
            # -----------------------------------------

            estimated_cost = round(
                quantity_prediction *
                equip["unit_cost_lakhs"] *
                specification_multiplier,
                2
            )
            # -----------------------------------------
            # BEST VENDOR SELECTION
            # -----------------------------------------

            best_vendor = vendor_engine.get_best_vendor(
                equip["equipment_id"]
            )
            risk_level, risk_reason = risk_engine.calculate_risk(
                best_vendor
            )

            # -----------------------------------------
            # PROCUREMENT ROUTE DECISION ENGINE
            # -----------------------------------------

            if equip["unit_cost_lakhs"] <= 5:

                procurement_route = "GeM Portal"

            elif equip["unit_cost_lakhs"] <= 25:

                procurement_route = "Open Tender"

            elif equip["unit_cost_lakhs"] <= 75:

                procurement_route = "Limited Tender"

            else:

                procurement_route = "Special Approval"


            total_estimated_cost += estimated_cost

            # -----------------------------------------
            # EXPLAINABILITY ENGINE
            # -----------------------------------------

            explanation = generate_explanation(

                municipality_data=muni,

                equipment_data=equip

            )

            explanation_text = " | ".join(
                explanation
            )
            
            
            
            
            recommendations.append({

                "Equipment":
                    equip["equipment_name"],

                "Specification":
                    best_vendor["Specification"],

                "Best Vendor":
                    best_vendor["Vendor"],

                "Vendor Rating":
                    best_vendor["Rating"],

                "Vendor Score":
                    best_vendor["Vendor Score"],
                    
                "Risk Level":
                    risk_level,

                "Risk Reason":
                    risk_reason,

                "GeM":
                    best_vendor["GeM"],

                "Quantity":
                    quantity_prediction,

                "Priority":
                    priority,

                "Estimated Cost":
                    estimated_cost,

                "Procurement Route":
                    procurement_route,

                "Category":
                    equip["procurement_category"]

            })

    result_df = pd.DataFrame(
        recommendations
    )

    # =========================================================
    # BUDGET ENGINE CALCULATION
    # =========================================================

    budget_result = calculate_budget_feasibility(

        annual_budget_lakhs=
            muni["annual_budget_lakhs"],

        procurement_cost_lakhs=
            total_estimated_cost

    )
    result_df = result_df.sort_values(
        by="Quantity",
        ascending=False
    )
    # =========================================================
    # ANALYTICS ENGINE
    # =========================================================

    analytics_result = generate_procurement_analytics(
        result_df
    )
    
   # =========================================================
# OPERATIONAL INDICATORS
# =========================================================

    st.markdown(
        '<div class="section-title">Infrastructure Deficit Indicators</div>',
        unsafe_allow_html=True
    )

# =========================================================
# MUNICIPAL ENGINEERING ALERTS
# =========================================================

    st.markdown(
        '<div class="section-title">Municipal Engineering Alerts</div>',
        unsafe_allow_html=True
    )
    # ---------------------------------------------------
# Calculate Engineering Indicators
# ---------------------------------------------------

    
    
    alerts = []

    if muni["water_supply_coverage_percent"] < 90:
        alerts.append("⚠ Water supply coverage below recommended level")

    if muni["drainage_coverage_percent"] < 85:
        alerts.append("⚠ Drainage coverage requires improvement")

    if muni["sewerage_coverage_percent"] < 85:
        alerts.append("⚠ Sewer network expansion recommended")

    if waste_processing_gap > 0:
        alerts.append(
            f"⚠ Waste processing deficit of {waste_processing_gap} TPD"
        )

    if muni["flood_risk_index"] >= 7:
        alerts.append("⚠ Municipality classified as High Flood Risk")

    if road_needing_repair > 50:
        alerts.append(
            f"⚠ Approximately {road_needing_repair} km of roads require improvement"
        )

    if not alerts:
        alerts.append("✅ No major engineering risks identified")

    for alert in alerts:
        st.warning(alert)



# ---------------------------------------------------
# ENGINEERING INDICATORS
# ---------------------------------------------------

    

    uncovered_water_population = round(
        muni["population"] *
        (100 - muni["water_supply_coverage_percent"]) / 100
    )

    uncovered_drainage_population = round(
        muni["population"] *
        (100 - muni["drainage_coverage_percent"]) / 100
    )

    

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Roads Needing Improvement",
            f"{road_needing_repair} km"
        )

    with col2:

        st.metric(
            "Population Without Water Coverage",
            f"{uncovered_water_population:,}"
        )

    with col3:

        st.metric(
            "Population Without Drainage",
            f"{uncovered_drainage_population:,}"
        )

    with col4:

        st.metric(
            "Waste Processing Gap",
            f"{waste_processing_gap} TPD"
        )
    
    
# =========================================================
# PROCUREMENT SUMMARY
# =========================================================

    st.markdown(
        '<div class="section-title">Procurement Intelligence Summary</div>',
        unsafe_allow_html=True
    )

    total_equipment = len(result_df)

    high_priority_count = len(
        result_df[
            result_df["Priority"] == "HIGH"
        ]
    )

    top_category = result_df[
        "Category"
    ].mode()[0]

    s1, s2, s3, s4 = st.columns(4)

    with s1:

        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-label">Equipment Approved for Procurement</div>
        <div class="metric-value">{total_equipment}</div>
        </div>
        """, unsafe_allow_html=True)

    with s2:

        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-label">Critical Equipment</div>
        <div class="metric-value">{high_priority_count}</div>
        </div>
        """, unsafe_allow_html=True)

    with s3:

        total_cost_cr = round(
            total_estimated_cost / 100,
            2
        )

        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-label">Estimated Procurement Cost</div>
        <div class="metric-value">₹ {total_cost_cr} Cr</div>
        </div>
        """, unsafe_allow_html=True)

    with s4:

        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-label">Priority Department</div>
        <div class="metric-value">{top_category}</div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# PROCUREMENT RECOMMENDATIONS TABLE
# =========================================================

    st.info(
        "The procurement recommendations below are generated using municipal infrastructure conditions, AI-based demand prediction, vendor evaluation, equipment criticality, and municipal procurement policy."
    )
    st.caption(
        f"Last Analysis Generated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}"
    )
    
    st.markdown(
        '<div class="section-title">Top Procurement Recommendations</div>',
        unsafe_allow_html=True
    )

    # Better table display than raw HTML

    styled_df = result_df.head(25).copy()

    def highlight_priority(val):

        if val == "HIGH":
            return """
            background-color:#DC2626;
            color:white;
            font-weight:bold;
            text-align:center;
            border-radius:6px;
            """

        elif val == "MEDIUM":
            return """
            background-color:#F59E0B;
            color:black;
            font-weight:bold;
            text-align:center;
            border-radius:6px;
            """

        else:
            return """
            background-color:#16A34A;
            color:white;
            font-weight:bold;
            text-align:center;
            border-radius:6px;
            """
    def highlight_risk(val):

        if val == "HIGH":
            return "background-color:#FECACA;color:#991B1B;font-weight:bold"

        elif val == "MEDIUM":
            return "background-color:#FEF3C7;color:#92400E;font-weight:bold"

        else:
            return "background-color:#DCFCE7;color:#166534;font-weight:bold"

    styled_table = (
        styled_df.style
        .map(
            highlight_priority,
            subset=["Priority"]
        )
        .map(
            highlight_risk,
            subset=["Risk Level"]
        )
    )

    st.dataframe(
        styled_table,
        use_container_width=True,
        height=500
    )

# =========================================================
# PROCUREMENT CHANNELS
# =========================================================

    st.markdown(
    '<div class="section-title">Procurement Route Distribution</div>',
    unsafe_allow_html=True
)

    route_summary = result_df[
        "Procurement Route"
    ].value_counts()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "GeM Portal",
            route_summary.get(
                "GeM Portal",
                0
            )
        )

    with col2:

        st.metric(
            "Open Tender",
            route_summary.get(
                "Open Tender",
                0
            )
        )

    with col3:

        st.metric(
            "Limited Tender",
            route_summary.get(
                "Limited Tender",
                0
            )
        )

    with col4:

        st.metric(
            "Special Approval",
            route_summary.get(
                "Special Approval",
                0
            )
        )


# =========================================================
# PROCUREMENT ANALYTICS DASHBOARD
# =========================================================

    # st.markdown(
    #     '<div class="section-title">Procurement Analytics Dashboard</div>',
    #     unsafe_allow_html=True
    # )
    # st.markdown(
    #     '<div class="section-title">AI Budget Optimizer</div>',
    #     unsafe_allow_html=True
    # )

    # col1, col2, col3 = st.columns(3)

    # with col1:
    #     st.metric(
    #         "Budget",
    #         f"₹ {budget_summary['Total Budget (Lakhs)']:.0f} L"
    #     )

    # with col2:
    #     st.metric(
    #         "Used",
    #         f"₹ {budget_summary['Budget Used (Lakhs)']:.0f} L"
    #     )

    # with col3:
    #     st.metric(
    #         "Remaining",
    #         f"₹ {budget_summary['Budget Remaining (Lakhs)']:.0f} L"
    #     )

    # col4, col5 = st.columns(2)

    # with col4:
    #     st.metric(
    #         "Approved",
    #         budget_summary["Approved Equipment"]
    #     )

    # with col5:
    #     st.metric(
    #         "Deferred",
    #         budget_summary["Deferred Equipment"]
    #     )

# -----------------------------------------
# PRIORITY DISTRIBUTION
# -----------------------------------------

    st.markdown(
        '<div class="section-title">Priority Distribution</div>',
        unsafe_allow_html=True  
    )

    priority_chart = analytics_result[
        "priority_distribution"
    ].set_index(
        "Priority"
    )

    st.bar_chart(
        priority_chart
    )

# -----------------------------------------
# PROCUREMENT ROUTE DISTRIBUTION
# -----------------------------------------

    st.markdown(
        '<div class="section-title">PROCUREMENT ROUTE DISTRIBUTION</div>',
        unsafe_allow_html=True  
    )

    route_chart = analytics_result[
        "route_distribution"
    ].set_index(
        "Procurement Route"
    )

    st.bar_chart(
        route_chart
    )

# -----------------------------------------
# CATEGORY DISTRIBUTION
# -----------------------------------------

    st.markdown(
        '<div class="section-title">CATEGORY DISTRIBUTION</div>',
        unsafe_allow_html=True  
    )

    category_chart = analytics_result[
        "category_distribution"
    ].set_index(
        "Category"
    )

    st.bar_chart(
        category_chart
    )
    
    # -----------------------------------------
# TOP COST EQUIPMENT
# -----------------------------------------

    st.markdown(
        '<div class="section-title">TOP COST EQUIPMENT</div>',
        unsafe_allow_html=True  
    )

    top_cost_df = analytics_result[
        "top_cost_equipment"
    ][[
        "Equipment",
        "Estimated Cost"
    ]]

    st.dataframe(
        top_cost_df,
        use_container_width=True
    )
# =========================================================
# EXPORT REPORT
# =========================================================

    st.markdown(
        '<div class="section-title">Export Procurement Report</div>',
        unsafe_allow_html=True
    )

    csv_data = result_df.to_csv(
        index=False
    )

    st.download_button(

        label="Download Procurement Report",

        data=csv_data,

        file_name=(
            selected_municipality +
            "_procurement_report.csv"
        ),

        mime="text/csv"
    )
    
    st.markdown("---")

   

# =========================================================
# EMPTY STATE
# =========================================================

else:

    st.info(
        "Select a municipality from the sidebar and click Generate Procurement Analysis."
    )



# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """

<div class="footer">

<hr>

<b>शहरMitra</b><br><br>

Municipal Procurement Intelligence Dashboard<br><br>

Internship Prototype | Infrastructure Recommendation Engine

</div>

""",
    unsafe_allow_html=True
)