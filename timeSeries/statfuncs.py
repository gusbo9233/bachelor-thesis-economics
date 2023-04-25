import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
from sklearn.linear_model import Lasso
import codes


def create_lagged_features(df, features, lag=1):
    lagged_df = df.copy()
    for feature in features:
        if codes.indicator_dict[feature] in lagged_df.columns:
            lagged_df[f"{codes.indicator_dict[feature]}_lag{lag}"] = lagged_df[codes.indicator_dict[feature]].shift(lag)
        else:
            print(f"Warning: Feature '{codes.indicator_dict[feature]}' not found in the DataFrame.")
    return lagged_df


def create_lagged_feature(df, target_feature, lead=1):
    lagged_df = df.copy()

    # Shift the target_feature forward (reverse-lag)
    if target_feature in lagged_df.columns:
        lagged_df[target_feature] = lagged_df[target_feature].shift(-lead)
    else:
        print(f"Warning: Feature '{target_feature}' not found in the DataFrame.")

    return lagged_df


def lasso_regress(country_code, alpha=1.0):
    # Load the merged CSV file
    data = pd.read_csv("merged_data.csv")
    data = data.drop(columns=['GDP per capita growth (annual %)'])

    # Create an imputer to fill missing values with the mean value of the respective column
    imputer = SimpleImputer(strategy="mean")

    # Extract the numeric columns
    numeric_data = data.select_dtypes(include=[np.number])

    # Fit the imputer and transform the numeric data
    numeric_data_filled = imputer.fit_transform(numeric_data)

    # Convert the filled numeric data back to a DataFrame with the same column names
    numeric_data_filled = pd.DataFrame(numeric_data_filled, columns=numeric_data.columns)
    numeric_data_filled.index = data.index

    # Drop the overlapping columns from the original data
    data = data.drop(columns=numeric_data.columns)

    # Combine the remaining non-numeric columns with the filled numeric data
    data_filled = data.join(numeric_data_filled)

    # Extract Rwanda (RWA) data into a separate DataFrame
    country_data = data_filled[data_filled['Country code'] == country_code]

    # Remove Rwanda (RWA) data from the main DataFrame
    data_filled = data_filled[data_filled['Country code'] != country_code]
    data_filled = data_filled.dropna(subset=["GDP growth (annual %)"])

    target = "GDP growth (annual %)"

    # Extract the feature columns (all columns except the target column)
    features = data_filled.columns.drop([target, 'Country code', 'Year'])

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(data_filled[features], data_filled[target], test_size=0.2,
                                                        random_state=42)

    # Create a Lasso regression model
    lasso_model = Lasso(alpha=alpha)

    # Fit the model to the training data
    lasso_model.fit(X_train, y_train)

    # Make predictions on the testing data
    y_pred = lasso_model.predict(X_test)

    # Calculate the mean squared error of the predictions
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean squared error: {mse}")

    # Print the estimated coefficients
    print("Coefficients:")
    for feature, coef in zip(features, lasso_model.coef_):
        print(f"{feature}: {coef}")

    # Print the intercept
    print(f"\nIntercept: {lasso_model.intercept_}")

    # Preprocess the Rwanda data
    X_rwanda = country_data[features].dropna()

    # Make predictions using the Lasso model
    country_gdp_growth_pred = lasso_model.predict(X_rwanda)

    # Add the predictions to the Rwanda DataFrame
    country_data.loc[X_rwanda.index, 'Predicted GDP growth (annual %)'] = country_gdp_growth_pred

    # Calculate the error metrics
    mae = mean_absolute_error(country_data['GDP growth (annual %)'].dropna(), country_gdp_growth_pred)
    rmse = np.sqrt(mean_squared_error(country_data['GDP growth (annual %)'].dropna(), country_gdp_growth_pred))

    print(f"Mean absolute error for Rwanda: {mae}")
    print(f"Root mean squared error for Rwanda: {rmse}")

    # Plot the actual vs. predicted GDP growth
    plt.figure(figsize=(10, 5))
    plt.plot(country_data['Year'], country_data['GDP growth (annual %)'], label='Actual GDP growth')
    plt.plot(country_data['Year'], country_data['Predicted GDP growth (annual %)'], label='Predicted GDP growth')
    plt.xlabel('Year')
    plt.ylabel('GDP growth (annual %)')
    plt.title(f'{country_code}: Actual vs. Predicted GDP growth using Lasso Regression')
    plt.legend()
    plt.show()

    # Save the updated Rwanda DataFrame to a CSV file
    country_data.to_csv('country_data_with_lasso_predictions.csv', index=False)


# lasso_regress("RWA",1)


def regress(country_code):
    # Load the merged CSV file
    data = pd.read_csv("series_data.csv")
    print(data.columns)
    data = create_lagged_feature(data, 'GDP per capita growth (annual %)')

    # data = data.drop(columns=['GDP growth (annual %)'])

    # Create an imputer to fill missing values with the mean value of the respective column
    imputer = SimpleImputer(strategy="mean")

    # Extract the numeric columns
    numeric_data = data.select_dtypes(include=[np.number])

    # Fit the imputer and transform the numeric data
    numeric_data_filled = imputer.fit_transform(numeric_data)

    # Convert the filled numeric data back to a DataFrame with the same column names
    numeric_data_filled = pd.DataFrame(numeric_data_filled, columns=numeric_data.columns)
    numeric_data_filled.index = data.index

    # Drop the overlapping columns from the original data
    data = data.drop(columns=numeric_data.columns)

    # Combine the remaining non-numeric columns with the filled numeric data
    data_filled = data.join(numeric_data_filled)

    # Extract Rwanda (RWA) data into a separate DataFrame
    country_data = data_filled[data_filled['Country code'] == country_code]

    # Remove Rwanda (RWA) data from the main DataFrame
    data_filled = data_filled[data_filled['Country code'] != country_code]
    data_filled = data_filled.dropna(subset=['GDP per capita growth (annual %)'])

    target = "GDP per capita growth (annual %)"

    # Extract the feature columns (all columns except the target column)
    features = data_filled.columns.drop([target, 'Country code', 'Year'])

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(data_filled[features], data_filled[target], test_size=0.2,
                                                        random_state=42)

    # Create a linear regression model
    regression_model = LinearRegression()

    # Fit the model to the training data
    regression_model.fit(X_train, y_train)

    # Make predictions on the testing data
    y_pred = regression_model.predict(X_test)

    # Calculate the mean squared error of the predictions
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean squared error: {mse}")

    # Print the estimated coefficients
    print("Coefficients:")
    for feature, coef in zip(features, regression_model.coef_):
        print(f"{feature}: {coef}")

    # Print the intercept
    print(f"\nIntercept: {regression_model.intercept_}")

    # Preprocess the Rwanda data
    X_rwanda = country_data[features].dropna()

    # Make predictions using the model
    country_gdp_growth_pred = regression_model.predict(X_rwanda)

    # Add the predictions to the Rwanda DataFrame
    country_data.loc[X_rwanda.index, 'Predicted GDP per capita growth (annual %)'] = country_gdp_growth_pred
    # Add the predictions to the Rwanda DataFrame
    country_data.loc[X_rwanda.index, 'Predicted GDP per capita growth (annual %)'] = country_gdp_growth_pred

    # Calculate the error metrics
    mae = mean_absolute_error(country_data['GDP per capita growth (annual %)'].dropna(), country_gdp_growth_pred)
    rmse = np.sqrt(
        mean_squared_error(country_data['GDP per capita growth (annual %)'].dropna(), country_gdp_growth_pred))

    print(f"Mean absolute error for {country_code}: {mae}")
    print(f"Root mean squared error for {country_code}: {rmse}")

    # Plot the actual vs. predicted GDP growth
    plt.figure(figsize=(10, 5))
    plt.plot(country_data['Year'], country_data['GDP per capita growth (annual %)'], label='Actual GDP growth')
    plt.plot(country_data['Year'], country_data['Predicted GDP per capita growth (annual %)'],
             label='Predicted GDP per capita growth')
    plt.xlabel('Year')
    plt.ylabel('GDP per capita growth (annual %)')
    plt.title(f' {country_code}: Actual vs. Predicted GDP per capita growth')
    plt.legend()
    plt.show()

    # Save the updated Rwanda DataFrame to a CSV file
    country_data.to_csv('country_data_with_predictions.csv', index=False)
    # Save the updated Rwanda DataFrame to a CSV file


# regress("RWA")
#regress("BDI")


def business_rankings():
    # Load the merged CSV file
    data = pd.read_csv("business_indicator_transformed3.csv")

    # Get the indicator columns that contain 'DFRN'
    # score_columns = [col for col in data.columns if 'score' in col]
    score_columns = [col for col in data.columns if any(indicator in col for indicator in codes.ease_of_business)]

    # Filter the data by selecting only the columns with 'DFRN'
    score_data = data[['Country code', 'Year'] + score_columns]
    # Fill missing values using forward-fill (ffill) method
    # score_data_filled = score_data.fillna(method='ffill')
    # for indicator, weight in codes.ease_of_business_weights.items():
    # indicator_columns = [col for col in score_data_filled.columns if indicator in col]
    # score_data_filled[indicator_columns] = score_data_filled[indicator_columns] * weight

    score_data_filled = score_data.copy()
    for column in score_columns:
        score_data_filled[column].fillna(score_data_filled[column].mean(), inplace=True)
    # Calculate the mean score for each country

    mean_scores = score_data_filled.groupby('Country code')[score_columns].mean()

    # Calculate the total score for each country
    total_scores = mean_scores.sum(axis=1)

    # Rank the countries based on their total scores
    rankings = total_scores.sort_values(ascending=False).reset_index()
    rankings.columns = ['Country code', 'Total score']

    # Print the ranking results
    print(rankings)


# business_rankings()


def business_rankings_growth():
    # Load the merged CSV file
    data = pd.read_csv("business_indicator_transformed3.csv")

    # Get the indicator columns that contain 'score'
    score_columns = [col for col in data.columns if 'score' in col]

    # Filter the data by selecting only the columns with 'score'
    score_data = data[['Country code', 'Year'] + score_columns]

    # Fill missing values using forward-fill (bfill) method
    score_data_filled = score_data.fillna(method='ffill')

    # Calculate the percentage growth for each country
    score_data_filled[score_columns] = score_data_filled.groupby('Country code')[score_columns].pct_change()

    # Calculate the mean growth for each country
    mean_growth = score_data_filled.groupby('Country code')[score_columns].mean()

    # Calculate the total growth for each country
    total_growth = mean_growth.sum(axis=1)

    # Rank the countries based on their total growth
    rankings = total_growth.sort_values(ascending=False).reset_index()
    rankings.columns = ['Country code', 'Total growth']

    # Print the ranking results
    print(rankings)


# business_rankings_growth()


# Call the regress function
# regress("BDI")
# regress("RWA")


# Call the function


def merge_collection2(collection):
    merged_data = None

    for key, df in collection.items():
        if df is None:
            continue
        # Transpose the DataFrame
        df = df.T

        # Set the column name to the key
        df.columns = [key]

        # If this is the first DataFrame, set it as the merged_data
        if merged_data is None:
            merged_data = df
        else:
            # Merge the current DataFrame with the merged_data DataFrame using the index
            merged_data = pd.merge(merged_data, df, left_index=True, right_index=True)

    return merged_data


def trim_to_common_timespan(collection):
    trimmed_collection = {}
    min_year = None
    max_year = None

    for key, df in collection.items():
        non_null_years = df.columns[df.notna().any()]
        current_min_year = int(non_null_years[0][2:])
        current_max_year = int(non_null_years[-1][2:])

        if min_year is None or current_min_year > min_year:
            min_year = current_min_year

        if max_year is None or current_max_year < max_year:
            max_year = current_max_year

    for key, df in collection.items():
        trimmed_df = df.loc[:, f"YR{min_year}":f"YR{max_year}"]
        trimmed_collection[key] = trimmed_df

    return trimmed_collection


def save_regression_model(model):
    with open("model.pk1", 'wb') as file:
        pickle.dump(model, file)
