import os 
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime

# Load the dotenv file:
load_dotenv(override=True)

# OpenAI:
api_key = st.secrets["OPENAI_API_KEY"]  #loading from Streamlit's secret section
MODEL = 'gpt-4o-mini'
openai = OpenAI()

    

def system_prompt(report_type=None, audience=None, include_recommendations=True):
    """
    A system prompt that tells the OpenAI on how to operate.
    """
    system_prompt = """
    You are a **Customer Retention Analyst** AI. Your task is to generate a concise, actionable report explaining customer churn risk, based on SHAP values and model predictions. Follow these rules:

    1. **Inputs**: 
       - A dictionary of SHAP values where positive values increase churn risk and negative values decrease it.
       - A binary churn prediction (1 = High Risk of Churn, 0 = Low Risk of Non-Churn).
       - A dictionary of input features that the model uses to predict whether a customer will Churn or Non-Churn. These were the
       features used to train this machine learning model.

    2. **Output Structure**:
       - **Title**: "Customer Churn Risk Report"

       - **Prediction**: State "High Risk (Predicted to Churn)" for prediction=1 or "Low Risk (Predicted to Retain)" for prediction=0.

       - **Top Drivers**: List the 3-5 most impactful features based on absolute SHAP values. For each feature:
          * Indicate whether it increases risk (positive SHAP) or decreases risk (negative SHAP)
          * Quantify the impact (e.g., "increases churn risk by approximately X%")

       - **Business Interpretation**: Explain what each top driver means in business terms.
    """
    
    # Customize based on report type
    if report_type:
        system_prompt += f"""
    3. **Report Type**: This should be a {report_type}. Follow these specific guidelines:
    """
        
        if report_type == "Executive Summary":
            system_prompt += """
       - Keep the report brief and focused on business impact (1-2 pages maximum)
       - Emphasize financial implications and ROI of recommendations
       - Use business terminology rather than technical terms
       - Include only high-level insights that would be relevant to executives
    """
        elif report_type == "Detailed Analysis":
            system_prompt += """
       - Provide deeper explanations of each factor
       - Include more context about how each feature affects churn
       - Add sections about potential underlying causes
       - Present a more comprehensive view with supporting details
    """
        elif report_type == "Technical Deep Dive":
            system_prompt += """
       - Include more technical details about the model and features
       - Discuss the statistical significance of each factor
       - Explain interactions between features when relevant
       - Use more precise technical language appropriate for data science teams
    """
        elif report_type == "Action Plan":
            system_prompt += """
       - Format the report primarily as a step-by-step action plan
       - Include specific actions, owners (by role), and timeframes
       - Focus heavily on the implementation details of recommendations
       - Include success metrics for measuring the impact of each action
    """
    
    # Customize based on audience
    if audience:
        system_prompt += f"""
    4. **Target Audience**: This report is intended for {audience}. Adjust your language and focus accordingly:
    """
        
        if audience == "Management":
            system_prompt += """
       - Focus on business impact, costs, and ROI
       - Use less technical jargon and more business terminology
       - Emphasize strategic implications rather than tactical details
       - Highlight competitive advantages of addressing churn issues
    """
        elif audience == "Customer Service Team":
            system_prompt += """
       - Focus on customer experience factors and touchpoints
       - Include practical guidance for customer interactions
       - Highlight service-related issues and how to address them
       - Use language that helps service teams understand customer frustration points
    """
        elif audience == "Technical Team":
            system_prompt += """
       - Include more technical details about the model and predictions
       - Discuss technical implementation of recommendations
       - Use appropriate technical terminology
       - Focus on system or product improvements that could reduce churn
    """
        elif audience == "Marketing Team":
            system_prompt += """
       - Focus on messaging, positioning, and customer segmentation
       - Include insights about customer preferences and behavior patterns
       - Suggest campaign ideas or promotional strategies to address churn risks
       - Use marketing terminology and concepts in your analysis
    """
    
    # Include or exclude recommendations based on checkbox
    if include_recommendations:
        system_prompt += """
    5. **Recommendations**: Suggest 2-3 specific, actionable interventions based on the top drivers. Each recommendation should:
       - Directly address one of the top factors driving churn
       - Be specific and actionable
       - Include an estimated impact level (high/medium/low)
       - Indicate implementation difficulty (easy/moderate/difficult)
    """
    
    
    
    # General style guidelines regardless of options
    system_prompt += """
    6. **Style**:
       - Use clear, appropriately technical language based on the audience
       - Correctly interpret SHAP values: Positive SHAP = increases churn probability; Negative SHAP = decreases churn probability
       - Focus only on features with significant SHAP values (absolute value > 0.01)
       - Base all insights strictly on the provided SHAP data and contextual information
       - Format the report with clear headings, bullet points, and readable organization
    """
    
    return system_prompt


def user_prompt(shap_values, predictions, customer_data, prediction_prob,  report_type=None, audience=None, include_recommendations=True):
    """
    A user prompt that tells OpenAI on what and how to respond.
    """
    
    # Format the prediction in a clearer way
    if isinstance(predictions, dict):
        prediction_text = "1 (Will Churn)" if predictions.get("prediction") == "Churn" else "0 (Will Not Churn)"
        probability = predictions.get("probability", 0.5)
    else:
        prediction_text = "1 (Will Churn)" if predictions == 1 else "0 (Will Not Churn)"
        probability = 0.5
    

    # Handle probability based on prediction to make it consistent
    if predictions == "Churn":
        probability = prediction_prob[0]  # probability of churning
        probability_text = f"{probability:.2f}% probability of churning"
    else:
        probability = prediction_prob[0]  # probability of staying
        probability_text = f"{probability:.2f}% probability of staying"
    # Create a dictionary of feature impacts if receiving raw SHAP values object
    if hasattr(shap_values, "values"):
        # Handle raw SHAP values object
        feature_impacts = {}
        # Logic to extract feature impacts from SHAP values object
    else:
        # Assume it's already a dictionary of feature impacts
        feature_impacts = shap_values
    
    # Sort by absolute magnitude to identify most important features
    sorted_shap = {k: v for k, v in sorted(feature_impacts.items(), key=lambda item: abs(item[1]), reverse=True)}
    
    user_prompt = f"""
    Generate a customer churn report using:
    - SHAP values: {sorted_shap}
    - Churn prediction: {prediction_text}
    - Churn probability: {probability}%
    - {probability_text}
    - Features used for the prediction: {customer_data}

    Additional context:
    - Current date: {datetime.now().strftime('%B %d, %Y')}
    """
    
    # Add customization details to the prompt
    if report_type:
        user_prompt += f"\nReport Type: {report_type}\n"
    
    if audience:
        user_prompt += f"Target Audience: {audience}\n"
    
    if include_recommendations:
        user_prompt += "\nInclude actionable recommendations based on the findings.\n"
    else:
        user_prompt += "\nDo NOT include recommendations in this report.\n"
    
    
    
    user_prompt += """
    Important notes for interpretation:
    1. In the provided SHAP values, POSITIVE values INCREASE churn risk, while NEGATIVE values DECREASE churn risk.
    2. Focus on the top 3-5 drivers with the highest absolute SHAP values.
    3. When interpreting the prediction: '1' means high risk (will churn), '0' means low risk (won't churn).
    4. Express SHAP values as percentages (e.g., a SHAP value of 0.05 = 5% impact on prediction).
    5. Format the report with clear headings and sections for readability.
    """
    
    return user_prompt


def get_report(shap_values, predictions, customer_data, prediction_prob, report_type=None, audience=None, include_recommendations=True):
    """
    A function that generates a streamed report using OpenAI's chat completions.
    """
    system = system_prompt(
        report_type=report_type, 
        audience=audience, 
        include_recommendations=include_recommendations, 
        
    )
    
    user = user_prompt(
        shap_values=shap_values, 
        predictions=predictions, 
        customer_data=customer_data,
        prediction_prob=prediction_prob,
        report_type=report_type,
        audience=audience, 
        include_recommendations=include_recommendations
    )
    
    input_data = [
        {"role": "system", "content": system},
        {"role": "user", "content": user}
    ]

    report_placeholder = st.empty()
    full_response = ""

    stream = openai.chat.completions.create(
        model=MODEL,
        messages=input_data,
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content:
            full_response += chunk.choices[0].delta.content
            report_placeholder.markdown(full_response)
    
    return full_response


