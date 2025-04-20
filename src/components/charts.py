import plotly.express as px
from src.data_processing.customer_data_access import  load_all_data, get_churn_count
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import shap
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


# Load the data (DB queries are replaced by a CSV file:):
data = pd.read_csv("data/churn_distribution.csv")
churn_count = data[data["churn"] == "Yes"]["count"].values

total_churn_count = churn_count[0]
# total_churn_count = get_churn_count()


total_customers =  data["count"].sum()
# total_customers = len(load_all_data())

baseline_churn_rate = (total_churn_count / total_customers) * 100


contract_mapping = {
    "Month-to-month": 6,
    "One year": 12,
    "Two year": 24
}


def display_churn_distribution(data, chart_key):
    """
    This function is responsible fetching the data from database and displaying the bar chart for churn and non-churn.
    """
    data = data
    custom_colors = {'Yes': '#b11346', 'No': '#0e7337'}
    st.write("")
    st.write("")
    st.subheader("Current Customer Churn Distribution")
    fig = px.bar(data, x='churn', y='count', color='churn', color_discrete_map=custom_colors)
    st.plotly_chart(fig, use_container_width=True, key=chart_key)
    st.write("")
    st.write("")
   
    


def display_customer_health_dashboard(res, input_features):
    """Displays the customer health dashboard based on the prediction"""


    prediction_prob = res.json()['Prediction_proba'] * 100
    delta_precentage = abs(baseline_churn_rate - prediction_prob)
    prediction = res.json()['Prediction']
    st.subheader("Customer Health Dashboard")
    
    m1, m2, m3 = st.columns(3)

    # Delta percentage:
    m1.metric("Churn Risk", 
            "🟢 Low" if prediction == 0 else "🔴 High",
            delta=f"{delta_precentage:.2f}% better than average" if prediction == 0 else f"{delta_precentage:.2f}% worse than average")
    
    # Prediction Probability:
    m2.metric(label= "Prediction Confidence", value=f"{prediction_prob:.2f}%", delta="Model's confidence")

    # Customer Life-Time Value:
    contract_length = contract_mapping.get(input_features["contract"])
    expected_remaining_tenure = max(contract_length - input_features["tenure"], 0)
    ltv = input_features["monthly_charges"] * expected_remaining_tenure

    m3.metric("Customer Life Time Value", f"{ltv:.2f} €", delta="Expected Amount")

    # Risk visualization
    risk_level = 100 - prediction_prob if prediction == 0 else prediction_prob
    st.write("Risk Level")
    st.progress(int(risk_level))

    st.write("")





def create_clean_shap_dashboard(customer_data, model, background_data=None):
    """
    Creates a clean two-row SHAP dashboard:
    - Top row: SHAP impact chart (without values on bars)
    - Bottom row: Feature values table
    """
    

    # ====================== [1. SHAP CALCULATIONS] ======================
    # Extract model components
    final_model = model.named_steps['model']
    preprocessor = model.named_steps['preprocessor']

    if isinstance(customer_data, dict):
        customer_df = pd.DataFrame([customer_data])
    else:
        customer_df = customer_data
    
    # Transform customer data
    X_transformed = preprocessor.transform(customer_df)
    if hasattr(X_transformed, "toarray"):
        X_transformed = X_transformed.toarray()
    
    # Get feature names
    if hasattr(preprocessor, 'get_feature_names_out'):
        feature_names = preprocessor.get_feature_names_out()
    else:
        feature_names = [f"feature_{i}" for i in range(X_transformed.shape[1])]
    
    # Create explainer
    if hasattr(final_model, 'predict_proba'):
        if hasattr(final_model, 'estimators_'):
            explainer = shap.TreeExplainer(final_model)
        elif hasattr(final_model, 'coef_'):
            explainer = shap.LinearExplainer(final_model, X_transformed)
        else:
            if background_data is not None:
                X_background = preprocessor.transform(background_data)
                if hasattr(X_background, "toarray"):
                    X_background = X_background.toarray()
                explainer = shap.KernelExplainer(final_model.predict_proba, X_background)
            else:
                explainer = shap.Explainer(final_model, X_transformed, feature_names=feature_names)
    else:
        explainer = shap.Explainer(final_model, X_transformed, feature_names=feature_names)
    
    # Get SHAP values
    if isinstance(explainer, shap.KernelExplainer):
        shap_values = explainer.shap_values(X_transformed)
        if isinstance(shap_values, list) and len(shap_values) > 1:
            shap_for_churn = shap_values[1] 
        else:
            shap_for_churn = shap_values
        base_value = explainer.expected_value
        if isinstance(base_value, list) and len(base_value) > 1:
            base_value = base_value[1]
    else:
        shap_values = explainer(X_transformed)
        if len(shap_values.shape) > 2 and shap_values.shape[2] > 1:
            shap_for_churn = shap_values[:, :, 1].values
            base_value = shap_values[0, :, 1].base_values
        else:
            shap_for_churn = shap_values.values
            base_value = shap_values.base_values
    
    # Feature mapping
    original_features = customer_df.columns.tolist()
    
    feature_mapping = {}
    for i, feature_name in enumerate(feature_names):
        parts = feature_name.split('__')
        if feature_name.startswith('encoding__') and len(parts) >= 2:
            full_feature = parts[1]
            for orig_feature in original_features:
                if full_feature.startswith(orig_feature):
                    feature_mapping[i] = orig_feature
                    break
            else:
                feature_mapping[i] = '_'.join(full_feature.split('_')[:-1])
        elif feature_name.startswith('remainder__') and len(parts) >= 2:
            feature_mapping[i] = parts[1]
        else:
            feature_mapping[i] = feature_name
    
    # Aggregate SHAP values
    aggregated_shap = {}
    for i, shap_value in enumerate(shap_for_churn[0]):
        original_feature = feature_mapping.get(i)
        if original_feature not in aggregated_shap:
            aggregated_shap[original_feature] = 0
        aggregated_shap[original_feature] += shap_value
    
    # Get customer values
    customer_values = {}
    for feature in original_features:
        if feature in customer_df.columns:
            customer_values[feature] = str(customer_df.iloc[0][feature])
    
    # Sort features by absolute impact
    sorted_features = sorted(aggregated_shap.keys(), 
                           key=lambda x: abs(aggregated_shap[x]), 
                           reverse=True)
    sorted_values = [aggregated_shap[f] for f in sorted_features]
    
    
    # ====================== [2. VISUALIZATION] ======================
    # Create figure with two rows
    fig = plt.figure(figsize=(18, 14))
    gs = fig.add_gridspec(2, 1, height_ratios=[2, 1], hspace=0.4)
    
    # ===== TOP ROW: CLEAN SHAP CHART (NO VALUES ON BARS) =====
    ax1 = fig.add_subplot(gs[0])
    
    # Visual parameters
    bar_height = 0.7
    y_pos = np.arange(len(sorted_features))
    colors = ['#0e7337' if x < 0 else '#b11346' for x in sorted_values]
    
    # Create clean bars without values
    ax1.barh(y_pos, sorted_values, height=bar_height, color=colors)
    
    # Chart styling
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(sorted_features, fontsize=12)
    ax1.set_xlabel('SHAP Value (Impact on Prediction)', fontsize=12)
    ax1.axvline(0, color='black', lw=0.8, alpha=0.5)
    ax1.grid(axis='x', linestyle='--', alpha=0.3)
    
    # ===== BOTTOM ROW: FEATURE TABLE =====
    ax2 = fig.add_subplot(gs[1])
    ax2.axis('off')
    
    # Prepare table data (now includes SHAP values since they're not on chart)
    table_data = [[f, customer_values.get(f, "N/A"), f'{aggregated_shap[f]:.2f}'] 
                 for f in sorted_features]
    
    # Create color map for table cells
    cmap = LinearSegmentedColormap.from_list('impact_cmap', ["#0e7337", "white", "#b11346"])
    max_impact = max(abs(v) for v in sorted_values)
    norm_values = [v/max_impact for v in sorted_values]
    
    # Create table
    table = ax2.table(
        cellText=table_data,
        colLabels=["Feature", "Customer Value", "SHAP Value"],
        loc='center',
        cellLoc='center',
        colWidths=[0.5, 0.3, 0.2],
        cellColours=[['white', 'white', cmap(0.5 + 0.5*n)] for n in norm_values]
    )
    
    # Table styling
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 1.8)  # Increase row height
    
    # Header styling
    for (row, col), cell in table.get_celld().items():
        if row == 0:  # Header row
            cell.set_text_props(weight='bold')
            cell.set_facecolor('#f7f7f7')
    
    # ===== PREDICTION TITLE =====
    prediction = model.predict(customer_df)[0]
    prediction_proba = model.predict_proba(customer_df)[0][1]
    fig.suptitle(
    f"Customer Churn Analysis "
    f"Prediction: {'Churn' if prediction == 1 else 'No Churn'} "
    f"(Probability: {(prediction_proba if prediction == 1 else (1 - prediction_proba)) * 100:.2f}% chance the customer will "
    f"{'leave' if prediction == 1 else 'stay'}) \n",
    fontsize=16, y=0.98
)
    
    # Final layout adjustment

    plt.subplots_adjust(top=0.94)  # Adjust top spacing
    
    
    return {
        "prediction": "Churn" if prediction == 1 else "No Churn",
        "churn_probability": float(prediction_proba),
        "plot": fig,
        "base_value": float(base_value),
        "shap_values": shap_values,
        "agg_shap": aggregated_shap,
        "customer_data" : customer_df
    }




def show_shap_top_features():
    """
    This function takes in the number of features that the user wants to see for the SHAP and shows the table and the chart.
    """
    shap_values = st.session_state.shap_values # session from explain.py
    input_features = st.session_state.input_features
    st.write(input_features)
    st.subheader("Explore Feature Importance with SHAP")
    n = st.number_input("Number of Features:", min_value=3, max_value=19, step=1)

    # Sorting the SHAP values:
    features_to_show = dict(sorted(shap_values.items(), key=lambda x: abs(x[1]), reverse=True)[:n])


    st.subheader(f"{n} Key Factors Influencing Prediction")
    features_to_show_df = pd.DataFrame([features_to_show]).T.reset_index()
    features_to_show_df.columns = ['Feature Name', 'Values']
    st.table(features_to_show_df)


    st.write("")
    features_to_show_df['Color'] = ['Descreases churn risk ↓' if v < 0 else 'Increases churn risk ↑' for v in features_to_show_df['Values']]
    # Plot with Plotly
    fig = px.bar(
        features_to_show_df,
        x='Feature Name',
        y='Values',
        color='Color',
        color_discrete_map={
            'Increases churn risk ↑': '#b11346',
            'Descreases churn risk ↓': '#0e7337'
        },
        title=f'Top {n} Most Impactful Features by SHAP Value',
        labels={'Color': 'Effect on Churn Risk'}
    )

    st.plotly_chart(fig, use_container_width=True)