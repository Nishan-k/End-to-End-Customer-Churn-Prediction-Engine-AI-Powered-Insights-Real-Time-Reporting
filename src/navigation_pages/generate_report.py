import streamlit as st  
from llm.report import get_report




def report_generation():
    """
    Reponsible for generating the report using OpenAI.
    """

    st.title("Generate Report Using LLM")

    st.write("Create a nice report for your stakeholder.")

    if st.button("Generate Report"):
        with st.spinner("Generating report..."):
            get_report(shap_values=st.session_state.shap_values, # session from explain.py
                       predictions=st.session_state.predictions, # session from explain.py
                       customer_data=st.session_state.input_features) # session from predict.py
        

