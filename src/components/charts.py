import plotly.express as px
import matplotlib.pyplot as plot
from src.data_processing.customer_data_access import get_churn_count, load_all_data
import streamlit as st




total_churn_count = get_churn_count()
total_customers =  len(load_all_data())
baseline_churn_rate = (total_churn_count / total_customers) * 100


contract_mapping = {
    "Month-to-month": 6,
    "One year": 12,
    "Two year": 24
}


def display_churn_distribution(data, chart_key):
    """
    This function is responsible fetching the data from database and displaying the bar chart for churn and non-churn.
    """
    data = data
    custom_colors = {'Yes': '#fc4903', 'No': '#03fc94'}
    st.write("")
    st.write("")
    st.subheader("Current Customer Churn Distribution:")
    fig = px.bar(data, x='churn', y='count', color='churn', color_discrete_map=custom_colors)
    st.plotly_chart(fig, use_container_width=True, key=chart_key)
    st.write("")
    st.write("")
   
    


def display_customer_health_dashboard(res, input_features):
    """Displays the customer health dashboard based on the prediction"""


    prediction_prob = res.json()['Prediction_proba'] * 100
    delta_precentage = abs(baseline_churn_rate - prediction_prob)
    prediction = res.json()['Prediction']
    st.subheader("Customer Health Dashboard")
    
    m1, m2, m3 = st.columns(3)

    # Delta percentage:
    m1.metric("Churn Risk", 
            "🟢 Low" if prediction == 0 else "🔴 High",
            delta=f"{delta_precentage:.2f}% better than average" if prediction == 0 else f"{delta_precentage:.2f}% worse than average")
    
    # Prediction Probability:
    m2.metric(label= "Prediction Confidence", value=f"{prediction_prob:.2f}%", delta="Model's confidence")

    # Customer Life-Time Value:
    contract_length = contract_mapping.get(input_features["contract"])
    expected_remaining_tenure = max(contract_length - input_features["tenure"], 0)
    ltv = input_features["monthly_charges"] * expected_remaining_tenure

    m3.metric("Customer Life Time Value", f"{ltv:.2f} €", delta="Expected Amount")

    # Risk visualization
    risk_level = 100 - prediction_prob if prediction == 0 else prediction_prob
    st.write("Risk Level")
    st.progress(int(risk_level))

    st.write("")