import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Use-Case Analyzer", layout="wide")

st.title("AI Enterprise Use-Case Identification & Feasibility Analyzer")
st.markdown("Consulting-Grade AI Transformation Assistant")

# -------------------------------------------------------
# INDUSTRY KNOWLEDGE BASE
# -------------------------------------------------------

industry_use_cases = {
    "Banking": [
        {"name": "Fraud Detection", "tech": "Supervised ML (Classification)"},
        {"name": "Credit Risk Scoring", "tech": "Logistic Regression / XGBoost"},
        {"name": "Customer Churn Prediction", "tech": "Predictive Modeling"},
        {"name": "AML Monitoring", "tech": "Anomaly Detection"},
    ],
    "Retail": [
        {"name": "Demand Forecasting", "tech": "Time-Series Forecasting"},
        {"name": "Dynamic Pricing", "tech": "Reinforcement Learning"},
        {"name": "Recommendation Engine", "tech": "Collaborative Filtering"},
        {"name": "Inventory Optimization", "tech": "Optimization + ML"},
    ],
    "Manufacturing": [
        {"name": "Predictive Maintenance", "tech": "Time-Series + IoT ML"},
        {"name": "Quality Inspection Automation", "tech": "Computer Vision"},
        {"name": "Supply Chain Optimization", "tech": "Optimization Models"},
        {"name": "Energy Consumption Forecasting", "tech": "Regression Models"},
    ],
    "Healthcare": [
        {"name": "Disease Prediction", "tech": "Classification Models"},
        {"name": "Patient Risk Stratification", "tech": "Predictive Analytics"},
        {"name": "Medical Image Analysis", "tech": "Deep Learning (CNN)"},
        {"name": "Hospital Resource Optimization", "tech": "Operations Research"},
    ],
}

# Complexity weights (consulting realism)
complexity_map = {
    "Fraud Detection": 0.8,
    "Credit Risk Scoring": 0.7,
    "Customer Churn Prediction": 0.6,
    "Demand Forecasting": 0.6,
    "Dynamic Pricing": 0.9,
    "Recommendation Engine": 0.7,
    "Inventory Optimization": 0.8,
    "Predictive Maintenance": 0.7,
    "Quality Inspection Automation": 0.9,
}

# -------------------------------------------------------
# SIDEBAR INPUTS
# -------------------------------------------------------

st.sidebar.header("Business Inputs")

industry = st.sidebar.selectbox("Select Industry", list(industry_use_cases.keys()))

objective = st.sidebar.selectbox(
    "Business Objective",
    ["Cost Reduction", "Revenue Growth", "Customer Experience", "ESG Strategy"],
)

pain_point = st.sidebar.text_area("Describe Business Pain Point")

data_availability = st.sidebar.selectbox("Data Availability", ["Low", "Medium", "High"])
budget_level = st.sidebar.selectbox("Budget Level", ["Low", "Medium", "High"])
timeline = st.sidebar.selectbox("Timeline", ["Short (<3 months)", "Medium (3-6 months)", "Long (>6 months)"])

# -------------------------------------------------------
# SCORING FUNCTIONS
# -------------------------------------------------------

def map_score(value):
    return {"Low": 0.3, "Medium": 0.6, "High": 1.0}[value]

def timeline_score(value):
    return {
        "Short (<3 months)": 0.4,
        "Medium (3-6 months)": 0.7,
        "Long (>6 months)": 1.0,
    }[value]

def calculate_base_feasibility():
    return (
        0.4 * map_score(data_availability)
        + 0.3 * map_score(budget_level)
        + 0.3 * timeline_score(timeline)
    )

def estimate_roi(objective):
    mapping = {
        "Cost Reduction": "10–20% operational cost savings",
        "Revenue Growth": "8–15% revenue uplift",
        "Customer Experience": "15–25% improvement in customer satisfaction",
        "ESG Strategy": "Improved ESG compliance and sustainability positioning",
    }
    return mapping[objective]

# -------------------------------------------------------
# MAIN LOGIC
# -------------------------------------------------------

if st.button("Generate AI Use Cases"):

    base_score = calculate_base_feasibility()
    roi_estimation = estimate_roi(objective)

    # Pain-point based filtering
    pain_lower = pain_point.lower()
    filtered_use_cases = []

    for uc in industry_use_cases[industry]:
        if "target" in pain_lower or "customer" in pain_lower:
            if "Recommendation" in uc["name"] or "Churn" in uc["name"]:
                filtered_use_cases.append(uc)
        elif "price" in pain_lower:
            if "Pricing" in uc["name"]:
                filtered_use_cases.append(uc)
        elif "stock" in pain_lower or "inventory" in pain_lower:
            if "Forecasting" in uc["name"] or "Inventory" in uc["name"]:
                filtered_use_cases.append(uc)

    if not filtered_use_cases:
        filtered_use_cases = industry_use_cases[industry][:2]

    # Generate results table
    results = []
    for uc in filtered_use_cases:
        complexity = complexity_map.get(uc["name"], 0.7)
        adjusted_score = round(base_score * complexity * 100, 2)

        results.append({
            "Use Case": uc["name"],
            "AI Technique": uc["tech"],
            "Feasibility Score (%)": adjusted_score,
            "Expected Impact": roi_estimation,
        })

    df = pd.DataFrame(results)

    st.header("Recommended AI Use Cases")
    st.dataframe(df, use_container_width=True)

    # -------------------------------------------------------
    # AI MATURITY LEVEL
    # -------------------------------------------------------

    st.header("AI Maturity Assessment")

    avg_score = df["Feasibility Score (%)"].mean()

    if avg_score > 75:
        maturity = "AI Mature"
    elif avg_score > 50:
        maturity = "AI Explorer"
    else:
        maturity = "AI Beginner"

    st.metric("AI Readiness Level", maturity)

    # -------------------------------------------------------
    # RISK MODEL
    # -------------------------------------------------------

    st.header("Risk Assessment")

    data_risk = "High" if data_availability == "Low" else "Medium"
    budget_risk = "High" if budget_level == "Low" else "Medium"
    timeline_risk = "High" if "Short" in timeline else "Medium"

    risk_df = pd.DataFrame({
        "Risk Type": ["Data Risk", "Budget Risk", "Timeline Risk"],
        "Risk Level": [data_risk, budget_risk, timeline_risk],
    })

    st.table(risk_df)

    # -------------------------------------------------------
    # EXECUTIVE SUMMARY
    # -------------------------------------------------------

    st.header("Executive Summary")

    summary = f"""
Client operating in the {industry} industry is currently facing:
"{pain_point}".

Based on structured feasibility assessment, recommended AI initiative is:
"{filtered_use_cases[0]['name']}" leveraging {filtered_use_cases[0]['tech']}.

Average Feasibility Score: {round(avg_score,2)}%

Expected Business Impact:
{roi_estimation}

Recommended Implementation Roadmap:
Phase 1 – Data Audit & Preparation  
Phase 2 – Pilot Model Development  
Phase 3 – Business Integration & Scaling  
Phase 4 – Monitoring & Optimization  

Key Strategic Risks:
- Data maturity constraints
- Budget limitations
- Organizational change resistance

This structured AI roadmap enables transformation while balancing feasibility and business impact.
"""

    st.write(summary)