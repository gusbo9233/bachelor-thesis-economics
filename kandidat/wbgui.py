import tkinter as tk
from tkinter import ttk
import wbgapi as wb
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

global current_data
indicators = set()
data_collections = {}


def fetch_and_plot_data(country_code, indicator_code):
    global current_data
    data = wb.data.DataFrame(indicator_code, country_code)
    print(data)
    current_data = data
    data = data.transpose()
    fig, ax = plt.subplots()
    data.plot(ax=ax)
    return fig


def save_data():
    global current_data
    indicator_name = entry_indicator_name.get()
    selected_item = collection_tree.selection()[0]  # Get the first selected item (assuming single selection)
    item_properties = collection_tree.item(selected_item)
    child_item = collection_tree.insert(selected_item, tk.END, text=indicator_name)
    data_collections[item_properties["text"]][indicator_name] = current_data


def new_collection(collection_name):
    data_collections[collection_name] = {}
    collection_tree.insert('', 'end', text=collection_name)


def on_plot_button_click():
    country_code = entry_country_code.get()
    indicator_code = entry_indicator_code.get()
    fig = fetch_and_plot_data(country_code, indicator_code)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=3, column=3)


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


def on_indicator_select(event):
    # Get the index of the selected item in the Listbox
    index = listbox.curselection()[0]
    # Get the selected item's text (indicator code)
    selected_indicator = listbox.get(index)
    # Delete any existing text in the indicator_entry and insert the selected indicator code
    entry_indicator_code.delete(0, tk.END)
    entry_indicator_code.insert(0, selected_indicator.split(':')[0])


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


root = tk.Tk()
root.geometry('1200x800')
label_country_code = tk.Label(root, text="Country Code:")
label_country_code.grid(row=0, column=0)
entry_country_code = tk.Entry(root)
entry_country_code.grid(row=0, column=1)

label_indicator_code = tk.Label(root, text="Indicator Code:")
label_indicator_code.grid(row=1, column=0)
entry_indicator_code = tk.Entry(root)
entry_indicator_code.grid(row=1, column=1)

button_plot = tk.Button(root, text="Plot", command=on_plot_button_click)
button_plot.grid(row=2, column=0)

button_fetch_indicators = tk.Button(root, text="Fetch Indicators", command=on_fetch_indicators_button_click)
button_fetch_indicators.grid(row=2, column=1)

scrollbar = tk.Scrollbar(root)
scrollbar.grid(row=3, column=2, sticky=tk.N + tk.S)

listbox = tk.Listbox(root, yscrollcommand=scrollbar.set, width=80, height=20)
listbox.grid(row=3, column=0, columnspan=2, sticky=tk.W + tk.E + tk.N + tk.S)
listbox.bind('<<ListboxSelect>>', on_indicator_select)  # Bind the on_indicator_select function to ListboxSelect event

collection_tree = ttk.Treeview(root)
collection_tree.grid(row=3, column=5)
entry_add_collection = tk.Entry(root)
entry_add_collection.grid(row=4, column=5)

button_add_collection = tk.Button(root, text="New Collection", command=on_add_collection_button_click)
button_add_collection.grid(row=5, column=5)

scrollbar.config(command=listbox.yview)

search_label = tk.Label(root, text="Search:")
search_label.grid(row=4, column=0, sticky=tk.W)

search_var = tk.StringVar()
search_var.trace('w', on_search_text_change)

search_entry = tk.Entry(root, textvariable=search_var)
search_entry.grid(row=4, column=1, sticky=tk.W + tk.E)

entry_indicator_name = tk.Entry(root)
entry_indicator_name.grid(row=6, column=5, sticky=tk.W + tk.E)

button_add_collection = tk.Button(root, text="Add data", command=on_add_data_button_click)
button_add_collection.grid(row=7, column=5)

button_add_collection = tk.Button(root, text="New Collection", command=on_add_collection_button_click)
button_add_collection.grid(row=5, column=5)

root.mainloop()
