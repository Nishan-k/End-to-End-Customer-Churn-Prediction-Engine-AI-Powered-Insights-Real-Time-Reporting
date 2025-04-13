import streamlit as st
import uuid 


from src.navigation_pages.home import home_intro
from src.data_processing.customer_data_access import get_churn_count
from src.components.charts import display_churn_distribution


# Navigation section:
page = st.sidebar.selectbox("Navigation Menu", ["🏠 Home", "📊 Predict", 
                                                "📖 Explain", "📑 Generate Report", "ℹ️ About"], key="page_selection")
st.sidebar.markdown("**🔍 Navigate through the sections to explore customer churn insights!**")
st.sidebar.markdown("")



# 1. Home Page:
if page == "🏠 Home":
    home_intro()
    st.write("")
    st.write("")
    st.subheader("Current Customer Churn Situation:")
    test = get_churn_count()
    test = test.rename(columns={"churn": "Churn", "count": "Total Churn Count"})
    st.write(test)

    graph_placeholder = st.empty()
    chart_key = f"chart_{uuid.uuid4()}"

    # Display the bar chart:
    with graph_placeholder.container():
        display_churn_distribution(chart_key=chart_key)


    # To update the chart if new data gets added to the customer table in the DB:
    if st.button("Update Graph"):
        chart_key = f"chart_{uuid.uuid4()}"
        with graph_placeholder.container():
            display_churn_distribution(chart_key=chart_key)