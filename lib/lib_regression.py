import pandas as pd
from sklearn.linear_model import LinearRegression

def perform_linear_regression(X_cols, y_col, data_file_path):
    # Load the data into a pandas dataframe
    data = pd.read_csv(data_file_path)

    # Split the data into independent variable (X) and the dependent variable (y)
    X = data[X_cols]
    y = data[y_col]

    # Create a LinearRegression object and fit the model to the data
    lr = LinearRegression()
    lr.fit(X, y)

    # Make a prediction for a new data point
    new_data = pd.DataFrame({col: [1.2] for col in X_cols})
    predicted_y = lr.predict(new_data)
    
    return predicted_y[0]