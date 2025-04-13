import plotly.express as px
import matplotlib.pyplot as plot
import streamlit as st

from src.data_processing.customer_data_access import get_churn_count







def display_churn_distribution(chart_key):
    """
    This function is responsible fetching the data from database and displaying the bar chart for churn and non-churn.
    """
    data = get_churn_count() 
    custom_colors = {'Yes': '#fc4903', 'No': '#03fc94'}
    st.write("")
    st.subheader("Current Customer Churn Distribution:")
    fig = px.bar(data, x='churn', y='count', color='churn', color_discrete_map=custom_colors)
    st.plotly_chart(fig, use_container_width=True, key=chart_key)


