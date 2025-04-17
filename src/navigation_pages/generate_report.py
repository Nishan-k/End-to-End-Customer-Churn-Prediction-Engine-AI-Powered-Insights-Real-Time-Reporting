import streamlit as st  
from llm.report import get_report
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def navigate_to_predict():
    st.session_state.page_selection = "📊 Predict"


def report_generation():
    """
    Reponsible for generating the report using OpenAI.
    """
    st.header("🧠 AI-Powered Churn Analysis Report")
    st.markdown("""
    Generate a comprehensive analysis of customer churn prediction with actionable insights 
    for stakeholders. The AI will analyze the prediction factors and provide tailored recommendations.
    """)
    


    if 'shap_values' not in st.session_state or 'predictions' not in st.session_state or 'customer_data' not in st.session_state:
        st.warning("⚠️ No prediction data available. Please make a prediction first.")
        if st.button("Go to Prediction Page", on_click=navigate_to_predict):
            return
        return
    
    shap_values = st.session_state.shap_values # session from explain.py
    predictions = st.session_state.predictions # session from explain.py
    customer_data = st.session_state.input_features # session from predict.py
    prediction_prob = st.session_state.pred_prob
    top_5_features = dict(sorted(shap_values.items(), key=lambda x: abs(x[1]), reverse=True)[:5])
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Prediction Result")
        if predictions == "Churn":
            st.error(f"⚠️ Customer Likely to Churn")
            pred = st.session_state.churn_prob
            st.markdown(f"**Churn Probability:** {pred:.2f}%")
        else:
            st.success(f"✅ Customer Likely to Stay")
            pred = st.session_state.non_churn_prob
            st.markdown(f"**Retention Probability:** {pred:.2f}%")
    
    with col2:
        st.subheader("5 Key Factors Influencing Prediction")
        top_5_features_df = pd.DataFrame([top_5_features]).T.reset_index()
        top_5_features_df.columns = ['Feature Name', 'Values']
        st.table(top_5_features_df)
    
    
    
    top_5_features_df['Color'] = ['Descreases churn risk ↓' if v < 0 else 'Increases churn risk ↑' for v in top_5_features_df['Values']]
    # Plot with Plotly
    fig = px.bar(
        top_5_features_df,
        x='Feature Name',
        y='Values',
        color='Color',
        color_discrete_map={
            'Increases churn risk ↑': '#b11346',
            'Descreases churn risk ↓': '#0e7337'
        },
        title='Top 5 Most Impactful Features by SHAP Value',
        labels={'Color': 'Effect on Churn Risk'}
    )

    st.plotly_chart(fig, use_container_width=True)
  
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
            get_report(shap_values=shap_values, 
                       predictions=predictions, 
                       customer_data=customer_data,
                       prediction_prob=prediction_prob,
                       report_type=report_type,
                       audience=audience,
                       include_recommendations=include_recommendations
                       ) 
        

