import pandas as pd
import re

# read in our csv
df = pd.read_csv('data/csv/ParkingViolations2015-Partial.csv', nrows=10000)
census2015 = (pd.read_csv('data/csv/census2015.csv', skiprows=1)).drop(["Id", "Id2"], axis=1)
census2016 = (pd.read_csv('data/csv/census2016.csv', skiprows=1)).drop(["Id", "Id2"], axis=1)
census2017 = (pd.read_csv('data/csv/census2017.csv', skiprows=1)).drop(["Id", "Id2"], axis=1)

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
# census parsing
census2015["Geography"] = census2015["Geography"].str.replace(" County, New York", "")
countyCheck = 0
for index, row in census2015.iterrows():
   for key in countyTranslations:
        if row["Geography"] in countyTranslations[key]:
            print(row["Geography"] in countyTranslations[key])
            countyCheck = 1

   if countyCheck == 0:
        census2015 = census2015[census2015.Geography != row["Geography"]]
   else:
       countyCheck = 0

census2015 = census2015.reset_index()
census2015 = census2015[census2015.columns[~census2015.columns.str.contains("error", flags=re.IGNORECASE)]]
census2015 = census2015[census2015.columns[~census2015.columns.str.contains("percent", flags=re.IGNORECASE)]]
filteredData = census2015[census2015.columns[census2015.columns.str.contains("(dollars)")]]
print("Columns Pulled From")
print("\n".join(list(filteredData.columns.str.split(" - "))))
mathFrame = pd.DataFrame()
mathFrame["Sum"] = round(filteredData.sum(axis=1), 2)
mathFrame["Avg"] = round(filteredData.sum(axis=1)/(len(filteredData.columns)), 2)
mathFrame["Full Name"] = census2015["Geography"]

print(mathFrame)




