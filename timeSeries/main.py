import wbgapi as wb

# Fetching population data for the United States (USA) for all years
for row in wb.data.fetch('SP.POP.TOTL', 'USA'):
    print(row)
