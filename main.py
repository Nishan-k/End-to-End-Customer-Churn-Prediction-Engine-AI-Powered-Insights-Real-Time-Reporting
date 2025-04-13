import streamlit as st

from src.pages.home import home_intro





page = st.sidebar.selectbox("Navigation Menu", ["🏠 Home", "📊 Predict", "📖 Explain", "📑 Generate Report", "ℹ️ About"],
                            key="page_selection")
st.sidebar.markdown("**🔍 Navigate through the sections to explore customer churn insights!**")
st.sidebar.markdown("")


if page == "🏠 Home":
    home_intro()
