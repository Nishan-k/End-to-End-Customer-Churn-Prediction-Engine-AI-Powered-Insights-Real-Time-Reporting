import streamlit as st  
from llm.report import get_report
from llm.pdf_generator import save_report_as_pdf
from datetime import datetime
import os 
import time

def navigate_to_predict():
    st.session_state.navigation_target = "📊 Predict"


def navigate_to_explain():
    st.session_state.navigation_target = "📖 Explain"


def report_generation():
    """
    Reponsible for generating the report using OpenAI.
    """
    st.header("🧠 AI-Powered Churn Analysis Report")
    st.markdown("""
    Generate a comprehensive analysis of customer churn prediction with actionable insights 
    for stakeholders. The AI will analyze the prediction factors and provide tailored recommendations.
    """)
    
   
    if 'customer_data' not in st.session_state or 'shap_values' not in st.session_state or 'predictions' not in st.session_state:
        st.warning("⚠️ This page requires session from explain page. Please go to the explanation page.")
        if st.button("Go to Explain Page", on_click=navigate_to_explain):
            return
        return

    
    shap_values = st.session_state.shap_values # session from explain.py
    predictions = st.session_state.predictions # session from explain.py
    customer_data = st.session_state.customer_data # session from predict.py
   
    
   
    st.subheader("Prediction Result")
    if predictions == "Churn":
        st.error(f"⚠️ Customer Likely to Churn")
        churn_pred = st.session_state.churn_prob
        st.markdown(f"**Churn Probability:** {churn_pred:.2f}%")
    else:
        st.success(f"✅ Customer Likely to Stay")
        non_churn_pred = st.session_state.non_churn_prob
        st.markdown(f"**Retention Probability:** {non_churn_pred:.2f}%")
  
    st.write("")
    

    st.markdown("---")
    st.subheader("Customize Your Report")
    
    col1, col2 = st.columns(2)
    with col1:
        report_type = st.selectbox(
            "Report Type",
            ["Executive Summary", "Detailed Analysis", "Technical Deep Dive", "Action Plan"]
        )
    
    with col2:
        audience = st.selectbox(
            "Target Audience",
            ["Management", "Customer Service Team", "Technical Team", "Marketing Team"]
        )
    
    include_recommendations = st.checkbox("Include Actionable Recommendations", value=True)


    if st.button("Generate Report"):
        with st.spinner("Generating report..."):  
            response = get_report(shap_values=shap_values, 
                    predictions=predictions, 
                    customer_data=customer_data,
                    prediction_prob=[churn_pred if predictions == "Churn" else non_churn_pred],
                    report_type=report_type,
                    audience=audience,
                    include_recommendations=include_recommendations
                    )      
            st.session_state.report_content = response
            

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        pdf_filename = f"Customer_churn_report_{timestamp}.pdf"
        pdf_path = save_report_as_pdf(report_text=st.session_state.report_content, pdf_filename=pdf_filename)
        if pdf_path is not None and os.path.exists(pdf_path):
            st.session_state.pdf_path = pdf_path
            time.sleep(2)
            with open(pdf_path, "rb") as file:
                st.download_button(
                    label="📥 Download as PDF",
                    data=file,
                    file_name=pdf_filename,
                    mime="application/pdf",
                    key="download_pdf"
                )
        else:
            st.error("⚠️ Failed to generate the PDF report. Please try again.")
            st.write("Debug info - pdf_path:", pdf_path)



        # if st.session_state.report_content and os.path.exists(st.session_state.pdf_path):
        #     with open(st.session_state.pdf_path, "rb") as file:
        #                         st.download_button(
        #                             label="📥 Download as PDF",
        #                             data=file,
        #                             file_name="Customer_churn_report.pdf",
        #                             mime="application/pdf",
        #                             key="download_pdf"
        #                         )
        # else:
        #      st.error("⚠️ Failed to generate the PDF report. Please try again.")
        #      st.write("Debug info - pdf_path:", st.session_state.pdf_path)

