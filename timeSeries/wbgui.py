import tkinter as tk
from tkinter import ttk

import requests
import wbgapi as wb
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import statfuncs as sf
import pickle
import os
import numpy as np
import codes
import pandas as pd

from fetcher import fetch_indicator_data

global current_data
global data_collections

indicators = set()


# data_collections = {}


def fetch_and_plot_data(country_code, indicator_code):
    global current_data
    data = wb.data.DataFrame(indicator_code, country_code)
    print(data)
    plt.close("all")

    current_data = data
    data = data.transpose()
    data.index = data.index.str.extract('(\d+)').squeeze().dropna().astype(int)

    fig, ax = plt.subplots()
    data.plot(ax=ax)
    first_year = data.index[0]
    last_year = data.index[-1]
    ax.set_xlim(first_year, last_year)
    ax.set_xticks(np.arange(first_year, last_year + 1, step=max(1, (last_year - first_year) // 10)))
    ax.set_xticklabels(np.arange(first_year, last_year + 1, step=max(1, (last_year - first_year) // 10)))
    return fig


def clear_all_data():
    global data_collections
    for country, series in data_collections.items():
        data_collections[country] = {}
    for parent in collection_tree.get_children():
        for child in collection_tree.get_children(parent):
            collection_tree.delete(child)

    update_tree()


def add_indicator(indicator_code):
    global data_collections
    fetched_data = fetch_indicator_data(indicator_code)

    for country, series in fetched_data.items():
        if country in data_collections:
            data_collections[country].update(series)
        else:
            data_collections[country] = series

    update_tree()


def click_add_series():
    indicator_code = entry_indicator_code.get()
    add_indicator(indicator_code)


def update_tree():
    global data_collections
    collection_tree.delete(*collection_tree.get_children())
    for country, series in data_collections.items():
        collection_item = collection_tree.insert("", "end", text=country)
        for indicator_name in series:
            collection_tree.insert(collection_item, "end", text=indicator_name)


def fetch_data_for_multiple_countries2(country_codes, indicator_codes, start_date=None, end_date=None):
    data = {}

    for country in country_codes:
        try:
            wb_country = wb.economy.get(country)
        except KeyError:
            print(f"Invalid country code: {country}")
            continue

        country_data = {}
        for indicator in indicator_codes:
            try:
                wb_indicator = wb.series.get(indicator)
            except KeyError:
                print(f"Invalid indicator code: {indicator}")
                continue

            try:
                if start_date is not None and end_date is not None:
                    series_data = wb.data.DataFrame(indicator, country, time=range(start_date, end_date + 1))
                else:
                    series_data = wb.data.DataFrame(indicator, country)

                country_data[indicator] = series_data
            except Exception as e:
                print(
                    f"Error fetching data for {wb_country.name} ({country}) and {wb_indicator.name} ({indicator}): {e}")
                continue

        data[country] = country_data

    return data


def fetch_data_for_multiple_countries(country_codes, indicator_codes):
    collections = {}
    for country_code in country_codes:
        collections[country_code] = {}
        for indicator_code in indicator_codes:
            try:
                data = wb.data.DataFrame(indicator_code, country_code)
                collections[country_code][indicator_code] = data
            except wb.APIResponseError as e:
                print(f"Error fetching data for country {country_code} and indicator {indicator_code}: {e}")
                # You can choose to either set the value as None or just not add it to the data_collections dictionary
                collections[country_code][indicator_code] = None
    return collections


def dump_timeseries_to_csv(output_dir='output'):
    global data_collections
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for country_code, country_data in data_collections.items():
        # Create a folder for each country
        country_folder = os.path.join(output_dir, country_code)
        if not os.path.exists(country_folder):
            os.makedirs(country_folder)

        for indicator_code, timeseries_data in country_data.items():
            if timeseries_data is None:
                print(f"No data available for {country_code} and {indicator_code}. Skipping.")
                continue
            if indicator_code not in codes.updated_indicator_dict.keys():
                continue

            # Create a CSV file for each indicator
            name = codes.updated_indicator_dict[indicator_code]
            csv_file_path = os.path.join(country_folder, f"{name}.csv")
            if type(timeseries_data) is not list:
                timeseries_data.to_csv(csv_file_path)

    print("Timeseries data successfully saved to CSV files.")


def fetch_doing_business_data(country_code, indicator_code):
    url = f"http://api.worldbank.org/v2/doingbusiness/country/{country_code}/indicator/{indicator_code}?format=json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching data: {response.status_code}")
        return None


def load_business_data():
    # Load the business indicator CSV file
    data = pd.read_csv("business_indicator.csv")
    business_data = data[data['Country Code'].isin(codes.ssa_country_codes)]

    indicators_df = pd.read_csv("DBSeries.csv")

    # Create a dictionary with 'Series Code' as keys and 'Indicator Name' as values
    business_updated_dict = dict(zip(data['Indicator Code'], indicators_df['Indicator Name']))
    # Your dictionary with indicator codes as keys and descriptions as values

    # Melt the dataframe
    melted_data = business_data.melt(id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
                                     var_name="Year", value_name="Value")

    # Replace indicator codes with descriptions
    melted_data['Indicator Code'] = melted_data['Indicator Code'].map(business_updated_dict)

    # Pivot the dataframe
    pivoted_data = melted_data.pivot_table(index=["Country Code", "Year"], columns="Indicator Code", values="Value",
                                           aggfunc='first').reset_index()

    # Rename the columns
    column_names = ['Country code', 'Year'] + pivoted_data.columns[2:].tolist()
    pivoted_data.columns = column_names

    # Save the transformed business indicator data to a CSV file
    pivoted_data.to_csv("business_indicator_transformed3.csv", index=False)


def on_load_click():
    global data_collections
    # Clear the existing treeview items
    collection_tree.delete(*collection_tree.get_children())

    # Define the list of country codes and indicator codes
    l = list(codes.indicators_new.keys())
    # Load the data using the load_country_data function
    data_collections = fetch_data_for_multiple_countries(country_codes, l)

    # Populate the treeview with the country data
    for country_code, indicators in data_collections.items():
        parent = collection_tree.insert("", "end", text=country_code)

        for indicator_code, time_series in indicators.items():
            collection_tree.insert(parent, "end", text=indicator_code)


def on_regression_click():
    global data_collections
    print(data_collections["RWA"]["NE.IMP.GNFS.ZS"])


def save_data():
    global current_data
    global data_collections

    indicator_name = entry_indicator_name.get()
    selected_item = collection_tree.selection()[0]  # Get the first selected item (assuming single selection)
    item_properties = collection_tree.item(selected_item)
    child_item = collection_tree.insert(selected_item, tk.END, text=indicator_name)
    data_collections[item_properties["text"]][indicator_name] = current_data


def delete_indicator():
    global data_collections
    indicator = entry_indicator_code.get()

    for country, series in data_collections.items():
        data_collections[country].pop(indicator)

    update_tree()


def new_collection(collection_name):
    global data_collections

    data_collections[collection_name] = {}
    collection_tree.insert('', 'end', text=collection_name)


def plot_selected_data(event):
    global data_collections

    selected_item = collection_tree.selection()[0]  # Get the first selected item (assuming single selection)
    item_properties = collection_tree.item(selected_item)

    if collection_tree.parent(selected_item):  # Check if the selected item has a parent (i.e., it's a child item)
        collection_name = collection_tree.item(collection_tree.parent(selected_item))['text']
        indicator_name = item_properties['text']
        entry_indicator_code.delete(0, tk.END)  # Delete existing text from the beginning (0) to the end (tk.END)
        entry_indicator_code.insert(0, indicator_name)  # Insert new text at the beginning (position 0)

        data = data_collections[collection_name][indicator_name]
        plt.close("all")

        # Plot the data
        data = data.transpose()
        data.index = data.index.str.extract('(\d+)').squeeze().astype(int)

        fig, ax = plt.subplots()
        first_year = data.index[0]
        last_year = data.index[-1]
        ax.set_xlim(first_year, last_year)
        ax.set_xticks(np.arange(first_year, last_year + 1, step=max(1, (last_year - first_year) // 10)))
        ax.set_xticklabels(np.arange(first_year, last_year + 1, step=max(1, (last_year - first_year) // 10)))

        data.plot(ax=ax)

        # Display the plot in the GUI
        canvas = FigureCanvasTkAgg(fig, master=content_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=5, column=0, columnspan=4, sticky=tk.W + tk.E)


def on_plot_button_click():
    country_code = entry_country_code.get()
    indicator_code = entry_indicator_code.get()
    fig = fetch_and_plot_data(country_code, indicator_code)

    # Create a new frame for the plot
    plot_frame = tk.Frame(content_frame)
    plot_frame.grid(row=5, column=0, columnspan=5)

    # Place the plot in the new frame
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def list_indicators(country_code):
    for series in wb.series.list():
        series_code = series['id']
        series_value = series['value']
        data = wb.data.fetch(series=series_code, economy=country_code)
        if data:
            indicators.add((series_code, series_value))
    return indicators


def on_fetch_indicators_button_click():
    country_code = entry_country_code.get()
    indicators = list_indicators(country_code)
    for code, value in indicators:
        listbox.insert(tk.END, f"{code}: {value}")


def on_add_collection_button_click():
    collection_name = entry_add_collection.get()
    new_collection(collection_name)


def describe_dataframes(collection):
    for indicator_name, data in collection.items():
        print(f"Indicator Name: {indicator_name}")
        print("Column Names:")
        print(data.columns)
        print("Data Types:")
        print(data.dtypes)
        print("Data Description:")
        print(data.describe())
        print("\n")


# Usage: describe_dataframes(your_collection)


def on_close():
    save_data_collections()
    root.destroy()


def save_data_collections():
    global data_collections

    with open("data_collections.pkl", "wb") as file:
        pickle.dump(data_collections, file)
    file.close()


def load_data_collections():
    global data_collections
    try:
        with open("data_collections.pkl", "rb") as file:
            data_collections = pickle.load(file)
    except FileNotFoundError:
        data_collections = {}


def on_indicator_select(event):
    index = listbox.curselection()[0]
    selected_indicator = listbox.get(index)
    entry_indicator_code.delete(0, tk.END)
    entry_indicator_code.insert(0, selected_indicator.split(':')[0].split(' ')[0].split('-')[0])


def on_add_data_button_click():
    save_data()


def update_indicators_list():
    # Clear the Listbox
    listbox.delete(0, tk.END)

    # Get the search text from the Entry
    search_text = search_var.get().lower()

    # Loop through the indicators and insert the ones that match the search text
    for indicator_code, indicator_name in indicators:
        if search_text in indicator_code.lower() or search_text in indicator_name.lower():
            listbox.insert(tk.END, f"{indicator_code} - {indicator_name}")


def on_search_text_change(*args):
    update_indicators_list()


def on_regression_button_click():
    global data_collections
    print(data_collections["RWA"]["NE.IMP.GNFS.ZS"].columns.values())


def validate_trimmed_dataframes(collection, save_directory='trimmed_data'):
    start_year = None
    end_year = None

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    for key, df in collection.items():
        years = [int(year[2:]) for year in df.columns]
        if start_year is None:
            start_year = years[0]
            end_year = years[-1]
        else:
            if start_year != years[0] or end_year != years[-1]:
                return False

        # file_path = os.path.join(save_directory, f"{key}_trimmed.csv")
        # df.to_csv(file_path)

    return True


def on_trim_click():
    global data_collections

    print("trim click")
    selected_item = collection_tree.selection()[0]  # Get the first selected item (assuming single selection)
    item_properties = collection_tree.item(selected_item)
    collection_name = item_properties["text"]
    collection = data_collections[collection_name]
    # describe_dataframes(collection)
    print(f"Trimmed data for the {collection} collection.")
    trimmed_collection = sf.trim_to_common_timespan(collection)
    data_collections[collection_name] = trimmed_collection
    is_valid = validate_trimmed_dataframes(trimmed_collection)

    if is_valid:
        print("The trimmed dataframes have the same start and end year.")
    else:
        print("The trimmed dataframes do not have the same start and end year.")


def remove_data():
    global data_collections

    selected_item = collection_tree.selection()[0]  # Get the first selected item (assuming single selection)
    item_properties = collection_tree.item(selected_item)
    parent_item = collection_tree.parent(selected_item)
    collection_name = collection_tree.item(parent_item)["text"]
    indicator_name = item_properties["text"]

    # Remove the data from the dictionary
    if collection_name in data_collections and indicator_name in data_collections[collection_name]:
        del data_collections[collection_name][indicator_name]

    # Remove the item from the treeview
    collection_tree.delete(selected_item)


# Your existing functions and global variables

root = tk.Tk()
root.title("World Bank Data Analysis")
root.geometry("1200x800")
root.protocol("WM_DELETE_WINDOW", on_close)

main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, sticky="nsew")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

canvas = tk.Canvas(main_frame)
canvas.grid(row=0, column=0, sticky="nsew")

main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)

x_scrollbar = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=canvas.xview)
x_scrollbar.grid(row=1, column=0, sticky="we")
y_scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
y_scrollbar.grid(row=0, column=1, sticky="ns")

canvas.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

content_frame = tk.Frame(canvas)

# Add other components with grid geometry manager
label_country_code = tk.Label(content_frame, text="Country Code:")
label_country_code.grid(row=0, column=0)
entry_country_code = tk.Entry(content_frame)
entry_country_code.grid(row=0, column=1)

label_indicator_code = tk.Label(content_frame, text="Indicator Code:")
label_indicator_code.grid(row=1, column=0)
entry_indicator_code = tk.Entry(content_frame)
entry_indicator_code.grid(row=1, column=1)

entry_nickname = tk.Entry(content_frame)
entry_nickname.grid(row=1, column=2)

button_plot = tk.Button(content_frame, text="Plot", command=on_plot_button_click)
button_plot.grid(row=2, column=0)

button_fetch_indicators = tk.Button(content_frame, text="Fetch Indicators", command=on_fetch_indicators_button_click)
button_fetch_indicators.grid(row=2, column=1)

scrollbar = tk.Scrollbar(content_frame)
scrollbar.grid(row=3, column=2, sticky=tk.N + tk.S)

listbox = tk.Listbox(content_frame, yscrollcommand=scrollbar.set, width=40, height=20)
listbox.grid(row=3, column=0, columnspan=2, sticky=tk.W + tk.E + tk.N + tk.S)
listbox.bind('<<ListboxSelect>>', on_indicator_select)

scrollbar.config(command=listbox.yview)

search_label = tk.Label(content_frame, text="Search:")
search_label.grid(row=4, column=0, sticky=tk.W)

search_var = tk.StringVar()
search_var.trace('w', on_search_text_change)

search_entry = tk.Entry(content_frame, textvariable=search_var)
search_entry.grid(row=4, column=1, sticky=tk.W + tk.E)

collection_tree = ttk.Treeview(content_frame)
collection_tree.grid(row=3, column=5, rowspan=5, sticky=tk.W + tk.E + tk.N + tk.S)

#entry_add_collection = tk.Entry(content_frame)
#entry_add_collection.grid(row=0, column=5, sticky=tk.W + tk.E)

#button_add_collection = tk.Button(content_frame, text="New Collection", command=on_add_collection_button_click)
#button_add_collection.grid(row=1, column=5)

entry_indicator_name = tk.Entry(content_frame)
entry_indicator_name.grid(row=9, column=5, sticky=tk.W + tk.E)

button_add_data = tk.Button(content_frame, text="Add data", command=on_add_data_button_click)
button_add_data.grid(row=10, column=5)

button_remove_data = tk.Button(content_frame, text="Remove data", command=remove_data)
button_remove_data.grid(row=11, column=5)

button_stat = tk.Button(content_frame, text="Load series for all", command=click_add_series)
button_stat.grid(row=0, column=6, padx=5, pady=5)

button_stat = tk.Button(content_frame, text="Regression", command=on_regression_click)
button_stat.grid(row=2, column=6, padx=5, pady=5)

button_load_data = tk.Button(content_frame, text="Load", command=on_load_click)
button_load_data.grid(row=3, column=6, padx=5, pady=5)

button_load_data = tk.Button(content_frame, text="Delete Indicator", command=delete_indicator)
button_load_data.grid(row=4, column=6, padx=5, pady=5)

load_data_collections()

update_tree()
collection_tree.bind('<<TreeviewSelect>>', plot_selected_data)
# clear_all_data()
entry_country_code.insert(0, "RWA")
on_fetch_indicators_button_click()
#dump_timeseries_to_csv()
# Place the content_frame in the canvas

country_codes = []
for country in wb.economy.list():
    country_codes.append(country['id'])


canvas.create_window((0, 0), window=content_frame, anchor=tk.NW)
content_frame.mainloop()
