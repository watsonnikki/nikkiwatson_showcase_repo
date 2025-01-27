import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import Lasso
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pickle

# Load the dataset
df1 = pd.read_csv('U.S._Chronic_Disease_Indicators.csv') # 2019 - 2022
df2 = pd.read_csv('U.S._Chronic_Disease_Indicators_old_data.csv') # 2011 - 2018

df = pd.concat([df1, df2], ignore_index=True)
print(df["YearEnd"].unique())

# Filter and clean your data as needed
filtered_df = df1.loc[df1['Question'] == 'Obesity among adults']
filtered_df = filtered_df.rename(columns={'Stratification1': 'Demographics'})
ml_df = filtered_df[['YearEnd', 'LocationDesc', 'Demographics', 'DataValue']]

ml_df.dropna(subset=['DataValue'], inplace=True)
ml_df['DataValue'] = ml_df['DataValue'].astype(float)

# Define your features and target variable
X = ml_df[['YearEnd', 'LocationDesc', 'Demographics']] 
y = ml_df['DataValue']

'''
These features (year, location, demographics) were chosen based on the EDA performed.
As evidenced in our graphs for obesity prevalence, there are clear trends among demographic 
groups, states, and year on obesity prevalence. 
The model was trained on these features in order to have the best chance of accurately 
predicting future prevalence of obesity. 
Additionally, when examining our data, we noticed that there are only four years, 2019-2022, 
and as such our models were finding very little correlation in obesity prevalence based on year. 
In order to predict future obesity rates, we decided that we needed data for additional years. 
We went to the CDC’s website and found an extended version of the US Chronic Disease Indicators dataset, 
and pulled obesity data from the years 2011 to 2018.
'''

# Preprocessing for categorical data: One-hot encoding
categorical_features = ['LocationDesc', 'Demographics']
preprocessor = ColumnTransformer(transformers=[
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)],
    remainder='passthrough')


"""
We evaluated each model using mean squared error, r-squared scores, and residual values. 
We evaluated three different models: a linear regression, a ridge model, and a Lasso model. 
The ridge model had an MSE of around 22 and an r-squared value of 0.61. 
The linear regression model had an MSE of around 14.9 and an r squared value of 0.75. 
The LASSO model had an MSE of around 23 with an r squared value of 0.61. 
Based on these values, we chose to use the Linear Regression model to predict the data.
"""

# Choose a model
model = Pipeline(steps=[
    ('poly', PolynomialFeatures(degree=2, include_bias=False)),
    ('reg', LinearRegression()) 
])

""" 
In order to get the best results, we introduced the interaction term of other significant 
factors and year. These interaction terms allow the model to capture the effect of each year
more accurately than just focus on the yearly data.
"""

# Create a pipeline that will encode the categories, create interaction terms, then fit the model
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('model', model)])

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the pipeline
pipeline.fit(X_train, y_train)

# Predict and evaluate
y_pred = pipeline.predict(X_test)

# Testing of models
mse = mean_squared_error(y_test, y_pred)
print(f'MSE: {mse}')

r2_score = r2_score(y_test, y_pred)
print(f'R2 Score: {r2_score}')

residuals = y_test - y_pred
print(f'Residuals: {residuals}')
print(f'Mean of residuals: {np.mean(residuals)}')
print(f'Min and Max of residuals are: {np.min(residuals)} and {np.max(residuals)}')

# To predict new values and testing accuracy of the model 
new_data = pd.DataFrame({
    'YearEnd': [2022],
    'LocationDesc': ['Michigan'],
    'Demographics': ['White, non-Hispanic']
})
predicted_dv = pipeline.predict(new_data)
print(f"The predicted percentage of obesity in {new_data['Demographics'][0]} people for {new_data['LocationDesc'][0]} in {new_data['YearEnd'][0]} is {predicted_dv[0]}")

new_data = pd.DataFrame({
    'YearEnd': [2025],
    'LocationDesc': ['Michigan'],
    'Demographics': ['White, non-Hispanic']
})
predicted_dv = pipeline.predict(new_data)
print(f"The predicted percentage of obesity in {new_data['Demographics'][0]} people for {new_data['LocationDesc'][0]} in {new_data['YearEnd'][0]} is {predicted_dv[0]}")

new_data = pd.DataFrame({
    'YearEnd': [2022],
    'LocationDesc': ['California'],
    'Demographics': ['White, non-Hispanic']
})
predicted_dv = pipeline.predict(new_data)
print(f"The predicted percentage of obesity in {new_data['Demographics'][0]} people for {new_data['LocationDesc'][0]} in {new_data['YearEnd'][0]} is {predicted_dv[0]}")


new_data = pd.DataFrame({
    'YearEnd': [2024],
    'LocationDesc': ['Nevada'],
    'Demographics': ['Asian, non-Hispanic']
})
predicted_dv = pipeline.predict(new_data)
print(f"The predicted percentage of obesity in {new_data['Demographics'][0]} people for {new_data['LocationDesc'][0]} in {new_data['YearEnd'][0]} is {predicted_dv[0]}")

new_data = pd.DataFrame({
    'YearEnd': [2030],
    'LocationDesc': ['Nevada'],
    'Demographics': ['Asian, non-Hispanic']
})
predicted_dv = pipeline.predict(new_data)
print(f"The predicted percentage of obesity in {new_data['Demographics'][0]} people for {new_data['LocationDesc'][0]} in {new_data['YearEnd'][0]} is {predicted_dv[0]}")

new_data = pd.DataFrame({
    'YearEnd': [2030],
    'LocationDesc': ['Nevada'],
    'Demographics': ['Overall']
})
predicted_dv = pipeline.predict(new_data)
print(f"The predicted percentage of obesity in {new_data['Demographics'][0]} people for {new_data['LocationDesc'][0]} in {new_data['YearEnd'][0]} is {predicted_dv[0]}")

new_data = pd.DataFrame({
    'YearEnd': [2030],
    'LocationDesc': ['Nevada'],
    'Demographics': ['Overall']
})
predicted_dv = pipeline.predict(new_data)
print(f"The predicted percentage of obesity in {new_data['Demographics'][0]} people for {new_data['LocationDesc'][0]} in {new_data['YearEnd'][0]} is {predicted_dv[0]}")

new_data = pd.DataFrame({
    'YearEnd': [2011],
    'LocationDesc': ['Nevada'],
    'Demographics': ['Overall']
})
predicted_dv = pipeline.predict(new_data)
print(f"The predicted percentage of obesity in {new_data['Demographics'][0]} people for {new_data['LocationDesc'][0]} in {new_data['YearEnd'][0]} is {predicted_dv[0]}")

new_data = pd.DataFrame({
    'YearEnd': [2080],
    'LocationDesc': ['Nevada'],
    'Demographics': ['Overall']
})
predicted_dv = pipeline.predict(new_data)
print(f"The predicted percentage of obesity in {new_data['Demographics'][0]} people for {new_data['LocationDesc'][0]} in {new_data['YearEnd'][0]} is {predicted_dv[0]}")

#Pickling the model
filename = 'ml_model.pkl'
pickle.dump(pipeline, open(filename, 'wb'))

ml_df.to_pickle('ml_df.pkl')