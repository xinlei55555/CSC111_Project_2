
import pandas as pd
import csv


def load_data_frame(living_costs_file: str, temperature_file: str) -> pd.DataFrame:
    """Return a dataframe containing information parsed from the living costs and temperature data files

    Data taken from the databases are as follows:
    Cost of living (all prices are in USD):
        - x12	Eggs (regular) (12)
        - x14	Chicken Fillets (1kg)
        - x16	Apples (1kg)
        - x23	Water (1.5 liter bottle, at the market)
        - x28	One-way Ticket (Local Transport)
        - x31	Taxi 1km (Normal Tariff)
        - x33	Gasoline (1 liter)
        - x36	Basic Utilities (Electricity, Heating, Cooling, Water, Garbage) for 85m2 Apartment
        - x38	Internet (60 Mbps or More, Unlimited Data, Cable/ADSL)
        - x42	Preschool (or Kindergarten), Full Day, Private, Monthly for 1 Child
        - x43	International Primary School, Yearly for 1 Child
        - x52	Price per Square Meter to Buy Apartment in City Centre
        - x53	Price per Square Meter to Buy Apartment Outside of Centre

    Temperature (all temperatures are in degrees celcius):
        - Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec,Year
    """
    cost_columns = [12, 14, 16, 23, 28, 31, 33, 36, 38, 42, 43, 52, 53]
    column_titles = ['City', 'Country', 'Eggs', 'Chicken', 'Apples', 'Water',
                     'Local Transport', 'Taxi', 'Gasoline', 'Utilities', 'Internet',
                     'Preschool', 'Primary School', 'Apartment in City',
                     'Apartment out of City', "Temperature-Jan", "Temperature-Feb",
                     "Temperature-Mar", "Temperature-Apr", "Temperature-May", "Temperature-Jun",
                     "Temperature-Jul", "Temperature-Aug", "Temperature-Sep", "Temperature-Oct",
                     "Temperature-Nov", "Temperature-Dec", "Temperature-Year", ]

    cities = {}

    with open(living_costs_file, 'r') as file:
        lines = csv.reader(file)
        for line in lines:
            if line[-1] == '1' and 'nan' not in line:  # excludes low sample size data and missing data
                cities[line[0]] = [line[1]]
                for i in cost_columns:
                    cities[line[0]].append(line[i + 1])

    with open(temperature_file, 'r') as file:
        lines = csv.reader(file)
        for line in lines:
            if line[1] in cities:
                cities[line[1]] += [temp.split('\n')[0] for temp in line[2:15]]

    c = []
    for city in cities:
        if len(cities[city]) == 27:
            c.append([city] + cities[city])

    df = pd.DataFrame(c, columns=column_titles)
    return df


if __name__ == '__main__':
    dataframe = load_data_frame('data/cost-of-living_v2.csv', 'data/Average Temperature of Cities.csv')
    print(dataframe)
