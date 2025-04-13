import streamlit as st


from src.pages.home import home_intro
from src.data_processing.customer_data_access import get_churn_count



# Navigation section:
page = st.sidebar.selectbox("Navigation Menu", ["🏠 Home", "📊 Predict", "📖 Explain", "📑 Generate Report", "ℹ️ About"],
                            key="page_selection")
st.sidebar.markdown("**🔍 Navigate through the sections to explore customer churn insights!**")
st.sidebar.markdown("")



# 1. Home Page:
if page == "🏠 Home":
    home_intro()
    test = get_churn_count()
    st.write(test)
