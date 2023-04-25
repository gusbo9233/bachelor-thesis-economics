import os
import pandas as pd


def process_csv(file_path, indicator, data_dict):
    df = pd.read_csv(file_path, header=None)
    country_code = file_path.split(os.path.sep)[-2]

    for year, value in zip(df.loc[0, 1:], df.loc[1, 1:]):
        key = (country_code, year[2:])
        data_dict[key][indicator] = value


root_folder = "output"
data_dict = {}

# Initialize the dictionary with empty lists for indicators
for folder in os.listdir(root_folder):
    folder_path = os.path.join(root_folder, folder)

    if os.path.isdir(folder_path):
        for file in os.listdir(folder_path):
            if file.endswith(".csv"):
                indicator = file[:-4]  # Remove .csv extension from the filename
                file_path = os.path.join(folder_path, f'{indicator}.csv')
                df = pd.read_csv(file_path, header=None)
                country_code = file_path.split(os.path.sep)[-2]

                for year in df.loc[0, 1:]:
                    key = (country_code, year[2:])
                    if key not in data_dict:
                        data_dict[key] = {indicator: None}
                    else:
                        data_dict[key][indicator] = None

# Process the files and populate the dictionary
for folder in os.listdir(root_folder):
    folder_path = os.path.join(root_folder, folder)

    if os.path.isdir(folder_path):
        for file in os.listdir(folder_path):
            if file.endswith(".csv"):
                indicator = file[:-4]  # Remove .csv extension from the filename
                file_path = os.path.join(folder_path, f'{indicator}.csv')
                process_csv(file_path, indicator, data_dict)

# Convert the dictionary to a DataFrame
merged_df = pd.DataFrame.from_dict(data_dict, orient='index')
merged_df.reset_index(inplace=True)
merged_df.columns = ['Country code', 'Year'] + list(merged_df.columns[2:])
merged_df.to_csv('series_data.csv', index=False)
