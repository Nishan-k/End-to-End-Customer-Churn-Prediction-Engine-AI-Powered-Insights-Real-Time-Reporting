import streamlit as st 
import requests
from src.components.charts import display_customer_health_dashboard
import pandas as pd


# def reset_prediction():
#     """
#     Reset all prediction-related session state variables
#     """

#     st.session_state.display_customer_health_dashboard = False
#     st.session_state.dashboard_data = False
  

#     keys_to_reset = [
#         "shap_values",
#         "predictions",
#         "report_content",
#         "pdf_path",
#         "churn_prob",
#         "non_churn_prob"
#     ]
#     for key in keys_to_reset:
#         if key in st.session_state:
#             del st.session_state[key]
    

    




def predict():
    """
    Takes the user input and makes a POST request via FastAPI for model prediction:
    """
    st.title("Churn Prediction")
    st.write("")

    with st.expander("⚠️ Note for Recruiters"):
                    st.write(
                        """
                        - **First prediction may take ~50 seconds** (Render free-tier cold start).  
                        - Subsequent requests will be faster (~5 sec).  
                        - Thank you for your patience!  
                        """
                            )
    st.write("")
    
    if 'display_customer_health_dashboard' not in st.session_state:
         st.session_state.display_customer_health_dashboard  = False
         st.session_state.dashboard_data = None
         
    
    if st.session_state.display_customer_health_dashboard:
        display_customer_health_dashboard(*st.session_state.dashboard_data)
        st.subheader("Given Input Features")
        df = pd.DataFrame([st.session_state.input_features]).T.reset_index()
        df.columns = ['Feature Name', 'Values']
        st.table(df)
        

   
        if st.button("Make New Prediction"):
            st.session_state.display_customer_health_dashboard = False
            st.session_state.dashboard_data = False

            sessions = ["input_features", "shap_values", "predictions", "customer_data"]
            for session in sessions:
                del st.session_state[session]

            st.rerun()


            

   
    if not st.session_state.display_customer_health_dashboard:
        st.subheader("Select Features Or Enter Data to Predict")
        st.write("")

        col1, col2 = st.columns([6, 6])

        with col1:
            gender = st.radio("Gender:", ("Male", "Female"))
            senior_citizen = st.radio("Is Senior Citizen?", ["Yes", "No"])
            partner = st.radio("Does the customer have a partner (e.g., spouse or significant other)?",["Yes", "No"])
            dependents = st.radio("Does the customer have dependents (e.g., children, spouse, or family members relying on you)?", ["Yes", "No"])
            tenure = st.number_input("Tenure (In Months):", min_value=1, max_value=100, step=1)
            phone_service = st.radio("Has Phone Service?", ["Yes", "No"])
            multiple_lines = st.radio("Has Multiple Lines?", ["Yes", "No"])
            internet_service = st.selectbox("Internet Service:", ["DSL", "Fibre optic", "No"])
            online_security = st.selectbox("Has intenet security?", ["Yes", "No","No internet service"])
            
        
        with col2:
            online_backup = st.selectbox("Has online backup?", ["Yes", "No", "No internet service"])
            device_protection = st.selectbox("Has Device Protection?", ["Yes", "No", "No internet service"])
            tech_support = st.selectbox("Has Tech Support?", ["Yes", "No", "No internet service"])
            streaming_tv = st.selectbox("Has Streaming TV?", ["Yes", "No", "No internet service"])
            streaming_movies = st.selectbox("Does Customer Stream Movies?", ["Yes", "No", "No internet service"])
            contract = st.radio("Contract Type:", ("One year", "Month-to-month", "Two year"))
            paperless_billing = st.radio("Has Paperless Billing?", ("Yes", "No"))
            payment_method = st.selectbox("Payment Method:", ["Mailed check", "Bank transfer (automatic)", "Electronic check", "Credit card (automatic)"])
            monthly_charges = st.number_input("Monthly Charge:", min_value=18.95, max_value=130.0, step=0.1)
            total_charges = st.number_input("Total Charge:", min_value=35.0, max_value=7900.0, step=0.1)

        if st.button("Predict Churn"):
                # Prepare data for API request
                input_features = {
                    "gender" : gender,
                    "senior_citizen" : senior_citizen,
                    "partner" : partner,
                    "dependents" : dependents,
                    "tenure" : tenure,
                    "phone_service" : phone_service,
                    "multiple_lines" : multiple_lines,
                    "internet_service" : internet_service,
                    "online_security" : online_security,
                    "online_backup" : online_backup,
                    "device_protection" : device_protection,
                    "tech_support" : tech_support,
                    "streaming_tv" : streaming_tv,
                    "streaming_movies" : streaming_movies,
                    "contract" : contract,
                    "paperless_billing" : paperless_billing,
                    "payment_method" : payment_method,
                    "monthly_charges" : round(monthly_charges, 2),
                    "total_charges" : round(total_charges, 2)
                }

        
      
                # Sending data to FastAPI for prediction
                res = requests.post(url="https://end-to-end-customer-churn-prediction-8ftp.onrender.com/predict", json=input_features)
                if res.status_code == 200:
                    st.session_state.input_features = input_features
                    st.write("")
                    display_customer_health_dashboard(res=res, input_features=input_features)
                    st.write("")
                    st.subheader("Given Input Features")
                    df = pd.DataFrame([st.session_state.input_features]).T.reset_index()
                    df.columns = ['Feature Name', 'Values']
                    st.table(df)                    
                    st.session_state.display_customer_health_dashboard = True
                    st.session_state.dashboard_data = (res, input_features)
                    st.write("")
                    st.write("")
                    st.info("👉Now, you can go to '📖 Explain' page or 📑 Generate Report page for further actions for this customer from the Navigation bar.")
                    st.write("")


               