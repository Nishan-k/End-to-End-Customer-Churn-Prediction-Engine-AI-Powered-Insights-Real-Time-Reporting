import pandas as pd
import joblib
import streamlit as st
from src.components.charts import create_clean_shap_dashboard



model = joblib.load("ml/churn_clf_model.pkl")


def explain():
    if 'input_features' not in st.session_state:
        st.warning("Please make a prediction first on the Predict page")
        return
    
    needs_recalculation = (
        "shap_result" not in st.session_state or 
        st.session_state.get('last_input_features') != st.session_state.input_features
    )


    if needs_recalculation:
        customer_data = pd.DataFrame.from_dict(
            {k: [v] for k, v in st.session_state.input_features.items()}
        )
        result = create_clean_shap_dashboard(customer_data=customer_data, model=model)
        st.session_state.shap_result = result
        st.session_state.customer_data = customer_data
        st.session_state.shap_values = result["shap_values"]
        st.session_state.last_input_features = st.session_state.input_features.copy()
    
    result = st.session_state.shap_result

    st.subheader("Prediction Result")
    prediction = result["prediction"]
    probability = result["churn_probability"] * 100

    # Display prediction with formatting
    if prediction == "Churn":
        st.error(f"Customer is predicted to churn with {probability:.1f}% probability")
    else:
        st.success(f"Customer is predicted to stay with {(100-probability):.1f}% probability")
    
    # Display the plot
    st.subheader("Feature Impact Analysis")
    st.pyplot(result["plot"])
    st.write("")
    st.write("")
    st.info("👉Now, you can go to '📖 Explain' page or '💡 Recommendations' or 📑 Generate Report page for further actions for this customer in the Navigation bar.")
    st.write("")