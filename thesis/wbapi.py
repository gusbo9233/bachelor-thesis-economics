import wbgapi as wb


# Fetching population data for the United States (USA) for all years
def test():
    for row in wb.data.fetch('SL.IND.EMPL.MA.ZS', 'RWA'):
        print(row)


def list_indicators(country_code):
    # Initialize an empty set for storing unique indicators
    indicators = set()

    # Iterate through all available indicators
    for series in wb.series.list():
        series_code = series['id']
        series_value = series['value']

        # Fetch data for the given country code and series code
        data = wb.data.fetch(series=series_code, economy=country_code)

        # If data is available, add the indicator to the set
        if data:
            indicators.add((series_code, series_value))

    return indicators


def check_country_code(country_code):
    for country in wb.economy.list():
        if country['id'] == country_code:
            return True
    return False


country_code = 'RW'
is_valid = check_country_code(country_code)
print(f"Is {country_code} a valid country code? {is_valid}")


def find_country_code(country_name):
    for country in wb.economy.list():
        if country['value'].lower() == country_name.lower():
            return country['id']
    return None


country_name = 'Rwanda'
country_code = find_country_code(country_name)
print(f"The country code for {country_name} is {country_code}")

country_code = "USA"  # Replace with the desired country code
indicators = list_indicators(country_code)
test()
