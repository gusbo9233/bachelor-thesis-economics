import codes
import wbgapi as wb
import pandas as pd


def fetch_indicator_data(indicator_code):
    data = {}
    for country in codes.ssa_country_codes:
        series = wb.data.DataFrame(indicator_code, country)
        data[country] = {}
        data[country][indicator_code] = series

    return data

