import streamlit as st
from prediction_helper import predict
import time
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="🏥 AI Health Insurance Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'show_prediction' not in st.session_state:
    st.session_state.show_prediction = False
if 'prediction_value' not in st.session_state:
    st.session_state.prediction_value = 0

# Simpler CSS for readability
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * { box-sizing: border-box; }

    .stApp {
        background: #2c3e50; /* Solid dark background for readability */
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }

    .main-hero {
        text-align: center;
        padding: 60px 20px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(25px);
        border-radius: 30px;
        margin: 20px 0 40px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.1);
    }

    .hero-title {
        font-size: clamp(2.5rem, 8vw, 5rem);
        font-weight: 800;
        color: #ecf0f1;
        margin-bottom: 20px;
    }

    .hero-subtitle {
        font-size: 1.4rem;
        color: rgba(255, 255, 255, 0.85);
        font-weight: 400;
        margin-bottom: 30px;
    }

    .form-section, .predict-section, .result-container {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 40px;
        margin: 30px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .section-header {
        font-size: 2rem;
        font-weight: 700;
        color: white;
        text-align: center;
        margin-bottom: 35px;
    }

    .input-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 25px;
    }

    .input-group label {
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 12px;
        display: block;
    }

    .predict-button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 20px 60px;
        font-size: 1.4rem;
        font-weight: 700;
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .predict-button:hover {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
    }

    .result-amount {
        font-size: clamp(3rem, 8vw, 5rem);
        font-weight: 800;
        color: white;
        margin: 25px 0;
    }

    .insight-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .insight-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 10px;
        display: block;
    }

    .insight-label {
        color: white;
        font-weight: 500;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# HERO SECTION
st.markdown("""
<div class="main-hero">
    <h1 class="hero-title">🏥 AI Health Insurance Predictor</h1>
    <p class="hero-subtitle">Advanced Machine Learning • Instant Accurate Predictions • Trusted by Thousands</p>
</div>
""", unsafe_allow_html=True)

# CATEGORICAL OPTIONS
categorical_options = {
    'Gender': ['Male', 'Female'],
    'Marital Status': ['Married', 'Unmarried'],
    'BMI Category': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
    'Smoking Status': ['No Smoking', 'Regular', 'Occasional'],
    'Employment Status': ['Salaried', 'Self-Employed', 'Freelancer'],
    'Region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'Medical History': [
        'No Disease', 'Diabetes', 'High Blood Pressure', 'Diabetes & High BP',
        'Thyroid', 'Heart Disease', 'BP & Heart Disease', 'Diabetes & Thyroid',
        'Diabetes & Heart Disease'
    ],
    'Insurance Plan': ['Bronze', 'Silver', 'Gold']
}

# PERSONAL INFO
st.markdown('<div class="form-section"><h2 class="section-header">👤 Personal Information</h2><div class="input-row">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="input-group"><label>🎂 Age</label></div>', unsafe_allow_html=True)
    age = st.slider('', 18, 100, 30)
    st.markdown('<div class="input-group"><label>⚧️ Gender</label></div>', unsafe_allow_html=True)
    gender = st.selectbox('', categorical_options['Gender'])
with col2:
    st.markdown('<div class="input-group"><label>💍 Marital Status</label></div>', unsafe_allow_html=True)
    marital_status = st.selectbox('', categorical_options['Marital Status'])
    st.markdown('<div class="input-group"><label>👨‍👩‍👦 Number of Dependants</label></div>', unsafe_allow_html=True)
    number_of_dependants = st.number_input('', 0, 20, 2)
with col3:
    st.markdown('<div class="input-group"><label>🌎 Region</label></div>', unsafe_allow_html=True)
    region = st.selectbox('', categorical_options['Region'])
    st.markdown('<div class="input-group"><label>🧬 Genetical Risk (0-5)</label></div>', unsafe_allow_html=True)
    genetical_risk = st.slider('', 0, 5, 2)
st.markdown('</div></div>', unsafe_allow_html=True)

# FINANCIAL INFO
st.markdown('<div class="form-section"><h2 class="section-header">💰 Financial Information</h2><div class="input-row">', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="input-group"><label>💰 Annual Income (Lakhs)</label></div>', unsafe_allow_html=True)
    income_lakhs = st.slider('', 0, 200, 15)
with col2:
    st.markdown('<div class="input-group"><label>💼 Employment Status</label></div>', unsafe_allow_html=True)
    employment_status = st.selectbox('', categorical_options['Employment Status'])
st.markdown('</div></div>', unsafe_allow_html=True)

# HEALTH INFO
st.markdown('<div class="form-section"><h2 class="section-header">🏥 Health & Lifestyle</h2><div class="input-row">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="input-group"><label>⚖️ BMI Category</label></div>', unsafe_allow_html=True)
    bmi_category = st.selectbox('', categorical_options['BMI Category'])
with col2:
    st.markdown('<div class="input-group"><label>🚬 Smoking Status</label></div>', unsafe_allow_html=True)
    smoking_status = st.selectbox('', categorical_options['Smoking Status'])
with col3:
    st.markdown('<div class="input-group"><label>🏥 Medical History</label></div>', unsafe_allow_html=True)
    medical_history = st.selectbox('', categorical_options['Medical History'])
st.markdown('</div></div>', unsafe_allow_html=True)

# INSURANCE PLAN
st.markdown('<div class="form-section"><h2 class="section-header">📜 Insurance Plan</h2><div class="input-row">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,1,1])
with col2:
    st.markdown('<div class="input-group"><label>📜 Insurance Plan Type</label></div>', unsafe_allow_html=True)
    insurance_plan = st.selectbox('', categorical_options['Insurance Plan'])
st.markdown('</div></div>', unsafe_allow_html=True)

# COLLECT INPUTS
input_dict = {
    'Age': age,
    'Number of Dependants': number_of_dependants,
    'Income in Lakhs': income_lakhs,
    'Genetical Risk': genetical_risk,
    'Insurance Plan': insurance_plan,
    'Employment Status': employment_status,
    'Gender': gender,
    'Marital Status': marital_status,
    'BMI Category': bmi_category,
    'Smoking Status': smoking_status,
    'Region': region,
    'Medical History': medical_history
}

# PREDICTION BUTTON
st.markdown('<div class="predict-section"><h2 style="color: white;">🔮 Get Your Prediction</h2></div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button('🎯 PREDICT MY INSURANCE COST'):
        st.session_state.show_prediction = True
        loading = st.empty()
        loading.markdown("🤖 AI is analyzing your profile...")
        time.sleep(2)
        loading.empty()
        try:
            prediction = predict(input_dict)
            st.session_state.prediction_value = prediction
            risk_score = 0
            if smoking_status == "Regular": risk_score += 3
            elif smoking_status == "Occasional": risk_score += 1
            if medical_history != "No Disease": risk_score += 2
            if bmi_category in ["Obesity", "Overweight"]: risk_score += 1
            if age > 50: risk_score += 1
            if risk_score <= 1:
                risk_level, risk_color = "Low", "#4CAF50"
            elif risk_score <= 3:
                risk_level, risk_color = "Medium", "#FF9800"
            else:
                risk_level, risk_color = "High", "#F44336"
            st.markdown(f"""
            <div class="result-container">
                <h3 style="color:white;">💰 Your Predicted Health Insurance Cost</h3>
                <div class="result-amount">₹{prediction:,}</div>
                <div class="insight-card"><span class="insight-value" style="color: {risk_color};">{risk_level}</span><div class="insight-label">Risk Level</div></div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Prediction failed: {e}")
