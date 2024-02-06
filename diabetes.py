# Import necessary libraries
import pandas as pd
import numpy as np 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


# Load the dataset
# Replace 'path_to_dataset' with the actual path to your dataset file
# the path to a dataset can be the path from your local machine 
# but to make the code more portable, you can use the relative path
dataset = pd.read_csv('./diabetes_prediction_dataset.csv')

# Split the dataset into features and target variable
X = dataset.drop('diabetes', axis=1)
y = dataset['diabetes']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train the model
model = LogisticRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Save the model
import joblib
joblib.dump(model, 'diabetes_model.joblib')
