import pandas as pd

# read in our csv
year = 2016
df = pd.read_csv('Parking_Violations_Issued_-_Fiscal_Year_' + str(year) + '.csv', nrows=50000)
df.to_csv('data/csv/ParkingViolations/nyc-parking-violations-partial-' + str(year) + '.csv')

# define map from county code to full name
countyTranslations = {
     'MN':'Manhattan',
     'NY':'Manhattan',
     'Q':'Queens',
     'QN':'Queens',
     'R':'Staten Island',
     'ST':'Staten Island',
     'K':'Brooklyn',
     'BK': 'Brooklyn',
     'BX':'Bronx',
     'nan':'null'
}

# print out our column headers
columnHeaders = list(df.columns.values)
print(columnHeaders)

df = pd.DataFrame(df, columns=['Violation County'])  # consider only the violation county column
df = df.groupby('Violation County')['Violation County'].count().reset_index(name='count')  # group by violation county, count unique, add count column
df['Full Name'] = df['Violation County'].map(countyTranslations)  # map from county code to full name
print(df)
