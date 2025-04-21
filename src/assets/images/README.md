# End-to-End-Customer-Churn-Prediction-Engine-AI-Powered-Insights-Real-Time-Reporting

<h3>The site is live, please feel free to visit:</h3>

<!-- *To Live Demo :  [End-to-end customer churn prediction model](https://end-to-end-customer-churn-prediction-engine-ai-powered.streamlit.app/)* -->


*To Live Demo :  <a href="https://end-to-end-customer-churn-prediction-engine-ai-powered.streamlit.app/" target="_blank">End-to-end customer churn prediction model</a>* *(Right-click to open in a new tab)*


![alt text](churn.jpg)

<hr>

*Image Source: [Customer Churn](https://www.universalcreativesolutions.com/insights/post/how-to-reduce-customer-churn-rate-ccr)*

<hr>

This is an end-to-end customer churn prediction app with FastAPI at the backend, ExtraTreesClassifier as the prediction model, Streamlit for the frontend, with SHAP explanations, and AI-generated retention reports.


The dataset that is used in this project was downloaded from Kaggle and here is the link to the dataset: 
*Data Source: [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)*


## Table of Contents

<ol>
<li><a href="#Overview"><b> Overview </a></b></li>
<li><a href="#Datasets"><b> Datasets </a></b></li>
<li><a href="#EDA"><b> Exploratory Data Analysis </a></b></li>
<li><a href="#datapreprocessing"><b> Data Preprocessing </a></b></li>
<li><a href="#spotchecking"><b> Spot Checking Algorithms </a></b></li>
<li><a href="#tuning"><b> Model Tuning </a></b></li>
<li><a href="#finalization"><b> Model Finalization </a></b></li>
<li><a href="#saveload"><b> Saving & Loading the Model </a></b></li>
<li><a href="#conclusion"><b> Conclusion </a></b></li>
</ol>


<h2 id="Overview">1. Overview</h2>
This project is an end-to-end Customer Churn Prediction App that integrates a FastAPI backend with an ExtraTreesClassifier machine learning model. The frontend is built using Streamlit, providing an interactive user interface. The app includes SHAP-based model interpretability to explain predictions and features AI-generated customer retention reports, offering actionable insights for business decision-making.


<h2 id="Datasets">2. Dataset</h2>
The data as downloaded as a CSV file from Kaggle and to mimic the real world scenario, a <b>Customer table</b> has been created and the data has been loaded in that table. For database, <b>PostgreSQL</b> has been used.
Then after authentication and creating a connection, a function <i>load_all_data()</i> is responsible to load the data from the database, which has been called in a Jupyter Notebook for machine learning tasks.

<h2 id="EDA">3. EDA</h2>

<h3> First the data is loaded: </h3>

![alt text](image.png)

<h3> Dimension of the dataset: </h3>

![alt text](image1.png)


<h3> Checking for NULL values: </h3>

![alt text](image-1.png)

<h3> Checking the data types: </h3>

![alt text](image-2.png)

![alt text](image-3.png)

<h3> Data Exploration with Visualization: </h3>

![alt text](image-5.png)

![alt text](image-6.png)

This is a pure case of class imbalance. As we can see, the classes are imbalanced, the count of Non-Churn is way higher than the count of the Churn.

<h3> Handling Class Imbalance: </h3>

![alt text](image-7.png)

Here, the minority class (Class 1) has been oversampled.

![alt text](image-8.png)

So, later on the stage, we will be using both the balanced Vs the imbalanced dataset and see on which datasets, the model will generate the best result and accordingly drop one of the dataset.

<h3> Visualizing Numerical Features: </h3>

<b> Histogram:</b>

![alt text](image-9.png)

<b> Density Plot:</b>

![alt text](image-10.png)


<b> Box Plot:</b>

![alt text](image-11.png)


<h2 id="#datapreprocessing">4. Data Preprocessing</h2>

<h3> Encoding: </h3>
The categorical data doesn't have Ordinal data, and these categorical data also doesn't have too much cardinality, so here, I will be using `One-hot Enoding` to encode these categorical data.

So, a function has been created that takes in a dataframe, separates the categorical and numerical features, performs `OneHotEncoder()` on categorical features, and returns the numerical features and the encoded categorical data as a dataframe.

<b> Encoding both original data(class imabalance dataset) and the balanced dataset:</b>

![alt text](image-12.png)

<h3> Correlation:</h3>

First, the correlation has been calculated and plotted as a heatmap for both original and balanced dataset:

<b> Correlation Heat Map for Original Dataset: </b>

![alt text](image-13.png)

<b> Correlation Heat Map for Balanced Dataset: </b>
![alt text](image-14.png)


<h3> Multi-Collinearity (VIF): </h3>

**NOTE:**  The threshold has been set as 10. VIF above the threshold of 10 would be considered having Multi-collinearity.


<b> Multi-collinearity test on original dataset:</b>


![alt text](image-15.png)


<b> Multi-collinearity test on balanced dataset:</b>

![alt text](image-16.png)



<h2 id="#spotchecking">5. Spot Checking Algorithms</h2>

