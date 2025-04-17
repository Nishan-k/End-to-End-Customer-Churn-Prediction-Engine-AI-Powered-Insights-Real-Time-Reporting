import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

def generate_report_page():
    st.title("🧠 AI-Powered Churn Analysis Report")
    
    st.markdown("""
    Generate a comprehensive analysis of customer churn prediction with actionable insights 
    for stakeholders. The AI will analyze the prediction factors and provide tailored recommendations.
    """)
    
    # Check if we have the necessary data
    if 'input_features' not in st.session_state or 'shap_result' not in st.session_state:
        st.warning("⚠️ No prediction data available. Please make a prediction first.")
        if st.button("Go to Prediction Page"):
            st.session_state.page_selection = "📊 Predict"
        return
        
    # Display prediction result prominently
    prediction = st.session_state.shap_result["prediction"]
    probability = st.session_state.shap_result["churn_probability"] * 100
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Prediction Result")
        if prediction == "Churn":
            st.error(f"⚠️ Customer Likely to Churn")
            st.markdown(f"**Probability:** {probability:.1f}%")
        else:
            st.success(f"✅ Customer Likely to Stay")
            st.markdown(f"**Retention Probability:** {(100-probability):.1f}%")
    
    with col2:
        st.subheader("Customer Profile")
        # Convert input features to DataFrame for display
        df = pd.DataFrame([st.session_state.input_features]).T.reset_index()
        df.columns = ['Feature', 'Value']
        
        # Display only the most relevant customer information
        important_features = ['tenure', 'MonthlyCharges', 'Contract', 'TotalCharges', 'PaymentMethod']
        filtered_df = df[df['Feature'].isin([f for f in important_features if f in df['Feature'].values])]
        st.table(filtered_df)
    
    # Show top influencing factors
    st.subheader("Key Factors Influencing Prediction")
    
    # Get the top factors from session state
    sorted_features = st.session_state.get("sorted_features", [])[:5]  # Get top 5
    sorted_values = st.session_state.get("sorted_values", [])[:5]
    
    # Create a horizontal bar chart of top factors
    if sorted_features and sorted_values:
        fig, ax = plt.figure(figsize=(10, 3)), plt.axes()
        colors = ['#FF4560' if x < 0 else '#008FFB' for x in sorted_values]
        ax.barh(sorted_features, sorted_values, color=colors)
        ax.set_xlabel('Impact on Prediction')
        ax.axvline(0, color='black', lw=0.8, alpha=0.5)
        st.pyplot(fig)
    
    # Report customization options
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
    include_visualizations = st.checkbox("Include Data Visualizations", value=True)
    
    # Generate report button
    st.markdown("---")
    generate_col, _, download_col = st.columns([2, 1, 1])
    
    with generate_col:
        if st.button("🚀 Generate Comprehensive Report", type="primary", use_container_width=True):
            report_placeholder = st.empty()
            report_placeholder.info("🧠 AI is analyzing customer data and generating insights...")
            
            # Here you'd call your streaming function
            # complete_report = get_report(
            #    st.session_state.shap_values, 
            #    {"prediction": prediction, "probability": probability},
            #    st.session_state.customer_data,
            #    report_type=report_type,
            #    audience=audience,
            #    include_recommendations=include_recommendations
            # )
            
            # For demonstration
            full_response = ""
            for i in range(10):
                time.sleep(0.3)
                full_response += "Generating report section... " * (i+1) + "\n\n"
                report_placeholder.info(full_response)
            
            report_placeholder.success("✅ Report generated successfully!")
            
    with download_col:
        st.download_button(
            "📥 Download Report",
            data="Your report content here",  # Replace with actual report content
            file_name="customer_churn_report.md",
            mime="text/markdown",
            disabled=True  # Enable after report is generated
        )