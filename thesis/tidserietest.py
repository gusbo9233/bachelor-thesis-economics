import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller


def co2_example():
    # Load CO2 dataset
    data = sm.datasets.co2.load_pandas().data
    data = data.dropna()  # Remove any missing values

    # Create a new DataFrame with the original data and an additional 'time' column
    data_with_time = data.assign(time=np.arange(len(data)))

    # Perform linear regression with the time variable as the independent variable and CO2 as the dependent variable
    X = sm.add_constant(data_with_time['time'])  # Add a constant for the intercept term
    y = data_with_time['co2']
    model = sm.OLS(y, X)
    results = model.fit()

    # Print the summary of the regression results
    print(results.summary())

    # Test for stationarity using the Augmented Dickey-Fuller test
    adf_result = adfuller(data['co2'])
    print('\nAugmented Dickey-Fuller Test:')
    print(f'ADF Statistic: {adf_result[0]}')
    print(f'p-value: {adf_result[1]}')
    print('Critical Values:')
    for key, value in adf_result[4].items():
        print(f'\t{key}: {value}')


def merge_example():
    data1 = pd.DataFrame({'A': np.random.rand(10), 'B': np.random.rand(10)})
    data2 = pd.DataFrame({'A': np.random.rand(10), 'B': np.random.rand(10)})
    data3 = pd.DataFrame({'A': np.random.rand(10), 'B': np.random.rand(10)})

    # Merge the DataFrames
    merged_data = pd.concat([data1, data2, data3], axis=0, ignore_index=True)

    # Add a time variable to the merged DataFrame
    merged_data['time'] = np.arange(len(merged_data))

    # Perform linear regression with the time variable as the independent variable and column 'A' as the dependent variable
    X = sm.add_constant(merged_data['time'])  # Add a constant for the intercept term
    y = merged_data['A']
    model = sm.OLS(y, X)
    results = model.fit()

    # Print the summary of the regression results
    print(results.summary())


merge_example()