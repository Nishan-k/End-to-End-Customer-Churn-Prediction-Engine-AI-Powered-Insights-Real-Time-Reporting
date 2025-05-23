# End-to-End-Customer-Churn-Prediction-Engine-AI-Powered-Insights-Real-Time-Reporting

<h3>The site is live, please feel free to visit:</h3>

<!-- *To Live Demo :  [End-to-end customer churn prediction model](https://end-to-end-customer-churn-prediction-engine-ai-powered.streamlit.app/)* -->


*To Live Demo :  <a href="https://end-to-end-customer-churn-prediction-engine-ai-powered.streamlit.app/" target="_blank">End-to-end customer churn prediction model</a>* *(Right-click to open in a new tab)*

<h2> Demo: How It Works   </h2>

![Demo GIF](https://github.com/Nishan-k/End-to-End-Customer-Churn-Prediction-Engine-AI-Powered-Insights-Real-Time-Reporting/blob/main/src/assets/images/demo.gif?raw=true)

<hr>



<hr>

This is an end-to-end customer churn prediction app with FastAPI at the backend, RandomForestClassifier as the prediction model, Streamlit for the frontend, with SHAP explanations, and AI-generated retention reports.


The dataset that is used in this project was downloaded from Kaggle and here is the link to the dataset: 
*Data Source: [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)*


## Table of Contents

<ol>
<li><a href="#Overview"><b> Overview </a></b></li>
<li><a href="#Datasets"><b> Datasets </a></b></li>
<li><a href="#EDA"><b> Exploratory Data Analysis </a></b></li>
<li><a href="#datapreprocessing"><b> Data Preprocessing </a></b></li>
<li><a href="#spotchecking"><b> Spot Checking Algorithms </a></b></li>
<li><a href="#optimization"><b> Hyper-Parameter Optimization </a></b></li>
<li><a href="#finalization"><b> Model Finalization </a></b></li>
<li><a href="#saveload"><b> Saving & Loading the Model </a></b></li>
<li><a href="#conclusion"><b> Conclusion </a></b></li>
</ol>


<h2 id="Overview">1. Overview</h2>
This project is an end-to-end Customer Churn Prediction App that integrates a FastAPI backend with an RandomForestClassifier machine learning model. The frontend is built using Streamlit, providing an interactive user interface. The app includes SHAP-based model interpretability to explain predictions and features AI-generated customer retention reports, offering actionable insights for business decision-making.


<h2 id="Datasets">2. Dataset</h2>
The data as downloaded as a CSV file from Kaggle and to mimic the real world scenario, a <b>Customer table</b> has been created and the data has been loaded in that table. For database, <b>PostgreSQL</b> has been used.
Then after authentication and creating a connection, a function <i>load_all_data()</i> is responsible to load the data from the database, which has been called in a Jupyter Notebook for machine learning tasks.

<h2 id="EDA">3. Exploratory Data Analysis</h2>

<h3> First the data is loaded: </h3>

![alt text](src/assets/images/image.png)

<h3> Dimension of the dataset: </h3>

![alt text](src/assets/images/image1.png)


<h3> Checking for NULL values: </h3>

![alt text](src/assets/images/image-1.png)

<h3> Checking the data types: </h3>

![alt text](src/assets/images/image-2.png)

![alt text](src/assets/images/image-3.png)

<h3> Data Exploration with Visualization: </h3>

![alt text](src/assets/images/image-5.png)

![alt text](src/assets/images/image-6.png)

This is a pure case of class imbalance. As we can see, the classes are imbalanced, the count of Non-Churn is way higher than the count of the Churn.

<h3> Handling Class Imbalance: </h3>

![alt text](src/assets/images/image-7.png)

Here, the minority class (Class 1) has been oversampled.

![alt text](src/assets/images/image-8.png)

So, later on the stage, we will be using both the balanced Vs the imbalanced dataset and see on which datasets, the model will generate the best result and accordingly drop one of the dataset.

<h3> Visualizing Numerical Features: </h3>

<b> Histogram:</b>

![alt text](src/assets/images/image-9.png)

<b> Density Plot:</b>

![alt text](src/assets/images/image-10.png)


<b> Box Plot:</b>

![alt text](src/assets/images/image-11.png)


<h2 id="datapreprocessing">4. Data Preprocessing</h2>


<h3> Encoding: </h3>
The categorical data doesn't have Ordinal data, and these categorical data also doesn't have too much cardinality, so here, I will be using `One-hot Enoding` to encode these categorical data.

So, a function has been created that takes in a dataframe, separates the categorical and numerical features, performs `OneHotEncoder()` on categorical features, and returns the numerical features and the encoded categorical data as a dataframe.

<b> Encoding both original data(class imabalance dataset) and the balanced dataset:</b>

![alt text](src/assets/images/image-12.png)

<h3> Correlation:</h3>

First, the correlation has been calculated and plotted as a heatmap for both original and balanced dataset:

<b> Correlation Heat Map for Original Dataset: </b>

![alt text](src/assets/images/image-13.png)

<b> Correlation Heat Map for Balanced Dataset: </b>
![alt text](src/assets/images/image-14.png)


<h3> Multi-Collinearity (VIF): </h3>

**NOTE:**  The threshold has been set as 10. VIF above the threshold of 10 would be considered having Multi-collinearity.


<b> Multi-collinearity test on original dataset:</b>


![alt text](src/assets/images/image-15.png)


<b> Multi-collinearity test on balanced dataset:</b>

![alt text](src/assets/images/image-16.png)



<h2 id="spotchecking">5. Spot Checking Algorithms</h2>

**NOTE:** 
Models that are used below: <br>
LR:  `LogisticRegression()` <br>
LDA:  `LinearDiscriminantAnalysis()` <br>
CART:  `DecisionTreeClassifier()` <br>
SVM:  `SVC()` <br>
NB:   `GaussianNB()` <br>
KNN: `KNeighborsClassifier()` <br>
AB: `AdaBoostClassifier()` <br>
GBM: `GradientBoostingClassifier` <br>
RF: `RandomForestClassifier()` <br>
ET:  `ExtraTreesClassifier()`


<h3> Spot Checking on Original Dataset: </h3>
So, first we will test out 6 algorithms then use Ensemble Models on the original dataset without scaling data then again we will scaled the data and compare the results:

<b> Train-Test split: </b>

<b> Original data unscaled: </b>

![alt text](src/assets/images/image-20.png)

Metrics:
![alt text](src/assets/images/image-17.png)

These `F1-Score` are not so good and `SVM` gave 0 for precision, recall and F1-score,  which shows how sensitive is it to unscaled data.

<b> Original data scaled: </b>
![alt text](src/assets/images/image-18.png)

After the data has been scaled, for `SVM` it went from 0 to 0.5064 for `F1-score` on scaled data.

Using `Ensemble Models` on the original dataset, as Ensemble model are robust to scalings, I will be using the original dataset directly without scaling them:

![alt text](src/assets/images/image-19.png)

<h3> Spot Checking on Blanaced Dataset: </h3>

<b> Train-Test split: </b>

![alt text](src/assets/images/image-21.png)

<b> Balanced data unscaled: </b>

Metrics:
![alt text](src/assets/images/image-22.png)

<b> Balanced data scaled: </b>

Metrics:

![alt text](src/assets/images/image-23.png)

<b> Balanced data Ensemble Models: </b>
Using `Ensemble Models` on the balanced dataset, as Ensemble model are robust to scalings, I will be using the balanced dataset directly without scaling them:

Metrics:
![alt text](src/assets/images/image-25.png)

Till now, `Ensemble Model` gave the best results, not just from the accuracy perspective, but other metrics like `F1-score, Precision, and Recall`. `Accuracy` is not a good metrics since our data has `Class Imbalance` problem, and in such scenario, other metrics should be considered.

So, till now, we have got two best models from the ensemble section and the best result was from the `balanced` dataset. So, I will be moving forward with the balanced dataset and those two models.

They are:
1. `ExtraTreesClassifier` and 
2. `RandomForest`

Now, I will be moving forward with these two models and optimize the `Hyper-parameter` using `GridSearchCV` and finalize the best model.


<h2 id="optimization">6. Hyper-Parameter Optimization</h2>
 
<b>  `RandomForestClassifier`  </b>

First, the `train-test` split is done:

![alt text](src/assets/images/image-26.png)

Then the `hyper-parameters` are defined as a dictionary:

![alt text](src/assets/images/image-27.png)

Then the `Random Forest` is trained on these combinations of  `hyper-parameters` and the best ones are saved as below:

![alt text](src/assets/images/image-28.png)

So, now, I have the best `hyper-parameters` for the `Random Forest` and these are used to re-train the model and fit on the training dataset:

![alt text](src/assets/images/image-29.png)

<b> Classification Report on `Training and Testing` : </b>

![alt text](src/assets/images/image-30.png)

<b> If we compare the `accuracy` the training data has `88%` while the testing data has `82%`, there is some overfitting. </b>

Now, let's move onto `ExtraTreesClassifier`.

<b> `ExtraTreesClassifier` </b>

The `hyper-parameters` are defined as a dictionary:

![alt text](src/assets/images/image-32.png)

![alt text](src/assets/images/image-34.png)

![alt text](src/assets/images/image-33.png)

The best `Hyper-parameters` for the `ExtraTreesClassifier`:

![alt text](src/assets/images/image-35.png)

<b> Re-train the `ExtraTreesClassifier` with the best `hyper-parameters`: </b>

![alt text](src/assets/images/image-36.png)

<b> Classification Report on both `Training and Testing` data: </b>

![alt text](src/assets/images/image-37.png)



**Conclusion:**

So, Random Forest performs better across all key metrics on the test set. So, the final model will be Random Forest.

<h2 id="finalization"> 7. Model Finalization </h2>

The model has been finalized, i.e. the final model will be `RandomForest` and will be trained with these hyper-parameters:

![alt text](src/assets/images/image-38.png)

So, the whole data is re-loaded usig the `load_all_data()` script. The `dtypes` will be changed as we did in the earlier phase as below and `customer_id` column will be dropped as we don't need it to build the model:

Load the data:
![alt text](src/assets/images/image-39.png)

Drop the column and change the `dtypes`:
![alt text](src/assets/images/image-40.png)


<b> Build the `Pipeline()` to avoid data-leakage: </b>

![alt text](src/assets/images/image-41.png)


<b> Split the data into `dependend` and `independent` features and fit the model: </b>

![alt text](src/assets/images/image-42.png)


![alt text](src/assets/images/image-43.png)




<h2 id="saveload">8. Saving & Loading the Model</h2>

Finally, we will save the model as a `pickle` file using `Joblib`:

![alt text](src/assets/images/image-44.png)


<b> Loading the model and making some predcitions: </b>

![alt text](src/assets/images/image-45.png)

<h3> Predicting on the first 3 values: </h3>

![alt text](src/assets/images/image-46.png)



<h2 id="conclusion">9. Conclusion</h2>

After training, testing, and hyper-parameter optimization, finally we have our final model. 

<b>Home Page:</b>
The home page is the landing page which shows the a table and a bar diagram of the current customer churn count in the database, the `Update Graph' will update the plot if new data gets appended to the database. This was the initial working nature when the application was build locally but during deployment the datbase was replaced by the CSV file as just for a single query, hosting the database didn't make sense but once I find the free alternative, the database will be deployed as well.

![alt text](src/assets/images/image-53.png)

![alt text](src/assets/images/image-54.png)

<b> Predict Page: </b>
The predict page contains the field to input the data from the user. In total, it contains 19 features which were used to train the model. `/preidct` endpoint has been created in FastAPI and has been deployed on render, so once the user inputs the feature and clicks the predict button, the data will be passed to the model `pipeline`, the prediction is returned and a customer dashboard will be shown as below:

![alt text](src/assets/images/image-47.png)

and also will list the features that were fed as an input to the prediction model.

<b> Explain Page: </b>
The explain page will display the SHAP (SHapley Additive exPlanations) values where these values provides an insights into how each input feature contributes to a prediction of the model.

It will show an entire data as below:
![alt text](src/assets/images/image-48.png)

But we can also drill down each feature and its values with 3 being the minimum number of features being displayed and 19 being the maximum number of features as 19 features were used in total for the model training:

![alt text](src/assets/images/image-49.png)

<b> Generate Report </b>
And finally we have a generate report section, that takes in the prediction result, SHAP values, the input features used for a particular customer, report type and the target audience and sends the data to the OpenAI via API request and generates a report for us:

![alt text](src/assets/images/image-50.png)

and once the report is generated, we can download it as a PDF file too.

Generating the report as a stream:

![alt text](src/assets/images/image-51.png)

and an option to download the generated report as a PDF file:

![alt text](src/assets/images/image-52.png)

