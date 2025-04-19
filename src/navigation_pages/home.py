import streamlit as st 
from src.assets.styles.styling import styled_write


image = "src/assets/images/churn.jpg"


# The intro section at the top of the page:
def home_intro():
    """
    This function is responsible to display the importance of customer churn for the business.
    """
    st.title("Customer Churn Prediction Model")
    st.write("")
    col1, col2 = st.columns([4, 4])
    with col1:
        styled_write("""
                Customer churn is the loss of customers over time. Predicting churn helps businesses 
                identify at-risk customers, take proactive retention measures, reduce acquisition costs, 
                and boost profitability through timely interventions like incentives and personalized services.
                    """)
    with col2:
        st.image(image)
        st.write("")
        st.write("")



