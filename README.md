# Economics Bachelor Thesis: Sub-Saharan African Economic Analysis

This repository contains the code, data, and analysis for my bachelor's thesis in economics focused on Sub-Saharan African economic indicators and development.

## Project Overview

This project analyzes economic indicators across Sub-Saharan African countries using data from the World Bank API. The thesis explores economic growth patterns, development indicators, and predictive modeling to understand factors influencing economic growth in the region.

## Repository Structure

- `main.py`: Simple example of fetching World Bank data
- `wbgui.py`: Main application with GUI interface for data visualization and analysis
- `statfuncs.py`: Statistical functions for data analysis and regression modeling
- `codes.py`: Country and indicator codes for Sub-Saharan African countries
- `fetcher.py`: Functions to fetch data from World Bank API
- `tobit.py`: Implementation of Tobit regression model
- `merged_data.csv`: Consolidated dataset with multiple indicators
- `series_data.csv`: Time series data for analysis
- `countries/`: Directory containing CSV files with country-specific data
- `Kandidatuppsatts.pdf`: The final thesis document (in Swedish)

## Features

- Fetch economic indicators from World Bank API
- Visualize time series data for different countries and indicators
- Perform regression analysis to identify relationships between indicators
- Create lag models for predictive analysis
- Generate comparative visualizations across countries

## Requirements

- Python 3.x
- Required packages:
  - pandas
  - numpy
  - matplotlib
  - scikit-learn
  - tkinter
  - wbgapi (World Bank API)

## Usage

1. Run the GUI application:
   ```
   python wbgui.py
   ```

2. Use the interface to:
   - Select countries and indicators
   - Visualize data with interactive plots
   - Add indicators to collections for analysis
   - Perform regression analysis
   - Export data to CSV files

## Data Sources

The data is sourced from the World Bank's World Development Indicators database using their API. Economic indicators include GDP growth, inflation rates, trade volumes, unemployment rates, and various sectoral contributions to GDP.

## License

This repository is for academic purposes. Please cite appropriately if using this work. 