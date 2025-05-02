import pandas as pd
import joblib
import streamlit as st
from src.components.charts import create_clean_shap_dashboard, show_shap_top_features


try:
    model = joblib.load("ml/churn_clf_model.pkl")
except Exception as e:
    st.error(f"Failed to load model: {e}")
    st.stop()

def navigate_to_predict():
    st.session_state.navigation_target = "📊 Predict"



    

def explain():
    """
    This function is responsible for displaying a SHAP chart and a table of SHAP values.
    """
    if 'input_features' not in st.session_state:
        st.warning("⚠️ No prediction data available. Please make a prediction first.")
        if st.button("Go to Prediction Page", on_click=navigate_to_predict):
            return  
        return  
    
    
    current_features = str(st.session_state.input_features)
    last_features = str(st.session_state.get('last_input_features', ""))
    
    needs_recalculation = (
        "shap_result" not in st.session_state or 
        current_features != last_features
    )

    if needs_recalculation:
        try:
            customer_data = pd.DataFrame.from_dict(
                {k: [v] for k, v in st.session_state.input_features.items()}
            )
            result = create_clean_shap_dashboard(customer_data=customer_data, model=model)
            st.session_state.update({
                "shap_result": result,
                "customer_data": customer_data,
                "shap_values": result["shap_values"],
                "last_input_features": st.session_state.input_features.copy()
            })
        except Exception as e:
            st.error(f"Error generating explanation: {e}")
            return

    
    result = st.session_state.get("shap_result")
    if not result:
        st.error("No explanation results available")
        return

    
    st.subheader("Prediction Result")
    prediction = result["prediction"]
    probability = result["churn_probability"] * 100
  

    if prediction == "Churn":
        st.error(f"Customer is predicted to churn with {probability:.2f}% probability")
        st.session_state.churn_prob = probability
    else:
        st.success(f"Customer is predicted to stay with {(100-probability):.2f}% probability")
        st.write(probability)
        st.session_state.non_churn_prob = 100 - probability
    
    st.subheader("Feature Impact Analysis of all the features")
    st.pyplot(result["plot"])
    
    st.session_state.update({
        "shap_values" : result["agg_shap"],
        "predictions": prediction
    })


    st.write("")
    show_shap_top_features()
 


    