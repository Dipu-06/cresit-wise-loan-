import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Loan Approval Predictor",
    page_icon="🏦",
    layout="wide",
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    background: linear-gradient(135deg,#0f172a,#1e293b);
}

.stApp {
    background: linear-gradient(135deg,#0f172a,#1e293b);
}

.hero {
    background: linear-gradient(135deg,#2563eb,#7c3aed);
    padding: 2rem;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.3);
}

.card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.1);
}

.metric-card {
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 15px;
    text-align:center;
}

h1,h2,h3,h4 {
    color:white;
}

label {
    color:white !important;
}

div[data-baseweb="select"] > div {
    background-color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown("""
<div class="hero">
<h1>🏦 AI Loan Approval Predictor</h1>
<p>Smart Credit Risk Assessment & Loan Eligibility Prediction</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------

# Replace with your trained model
# model = joblib.load("loan_model.pkl")

# Dummy Prediction Function
def predict_loan(features):

    income = features["income"]
    credit_score = features["credit_score"]
    loan_amount = features["loan_amount"]

    score = (
        (credit_score/900)*50 +
        (income/100000)*30 -
        (loan_amount/500000)*20
    )

    return 1 if score > 40 else 0, round(score,2)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    width=120
)

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select",
    ["Loan Predictor","About Project"]
)

# ---------------------------------------------------
# ABOUT PAGE
# ---------------------------------------------------

if page == "About Project":

    st.markdown("""
    ## Project Overview

    This project uses Machine Learning to predict whether a loan application is likely to be approved.

    ### Features
    - Credit Risk Analysis
    - Real-time Prediction
    - Financial Dashboard
    - Professional UI
    - Streamlit Deployment Ready

    ### Tech Stack
    - Python
    - Streamlit
    - Scikit-Learn
    - Pandas
    - NumPy

    ### Future Improvements
    - XGBoost Model
    - SHAP Explainability
    - Database Integration
    - PDF Report Generation
    """)

# ---------------------------------------------------
# PREDICTOR PAGE
# ---------------------------------------------------

else:

    col1, col2 = st.columns([2,1])

    with col1:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.subheader("Applicant Information")

        gender = st.selectbox(
            "Gender",
            ["Male","Female"]
        )

        married = st.selectbox(
            "Married",
            ["Yes","No"]
        )

        education = st.selectbox(
            "Education",
            ["Graduate","Not Graduate"]
        )

        employment = st.selectbox(
            "Self Employed",
            ["Yes","No"]
        )

        income = st.number_input(
            "Monthly Income (₹)",
            min_value=0,
            value=50000
        )

        co_income = st.number_input(
            "Co-applicant Income (₹)",
            min_value=0,
            value=10000
        )

        loan_amount = st.number_input(
            "Loan Amount (₹)",
            min_value=10000,
            value=200000
        )

        loan_term = st.slider(
            "Loan Term (Months)",
            12,
            480,
            240
        )

        credit_score = st.slider(
            "Credit Score",
            300,
            900,
            700
        )

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="metric-card">
        <h3>Financial Summary</h3>
        </div>
        """, unsafe_allow_html=True)

        st.metric(
            "Income",
            f"₹{income:,}"
        )

        st.metric(
            "Loan Amount",
            f"₹{loan_amount:,}"
        )

        st.metric(
            "Credit Score",
            credit_score
        )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "🔍 Predict Loan Approval",
        use_container_width=True
    ):

        features = {
            "income": income,
            "co_income": co_income,
            "loan_amount": loan_amount,
            "loan_term": loan_term,
            "credit_score": credit_score
        }

        prediction, risk_score = predict_loan(features)

        st.markdown("## Prediction Result")

        st.progress(
            min(int(risk_score),100)
        )

        st.metric(
            "Eligibility Score",
            f"{risk_score}%"
        )

        if prediction == 1:

            st.success(
                "✅ Loan Approved"
            )

            st.balloons()

        else:

            st.error(
                "❌ Loan Rejected"
            )

        report = pd.DataFrame({
            "Feature":[
                "Income",
                "Co Income",
                "Loan Amount",
                "Loan Term",
                "Credit Score"
            ],
            "Value":[
                income,
                co_income,
                loan_amount,
                loan_term,
                credit_score
            ]
        })

        st.subheader("Application Summary")
        st.dataframe(
            report,
            use_container_width=True
        )