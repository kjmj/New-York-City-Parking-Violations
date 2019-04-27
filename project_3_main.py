import pandas as pd
import re


def cleanCols(dataframe):
    for column in dataframe:
        columnError = 0
        valsTested = 0
        for i, row in dataframe.iterrows():
            valsTested += 1
            try:
                float(row[column])
            except ValueError:
                columnError += 1
        if columnError/valsTested >= 0.6:
            dataframe = dataframe.drop(columns=column)
    return dataframe


# read in our csv
df = pd.read_csv('data/csv/ParkingViolations2015-Partial.csv', nrows=10000)
merged2015 = pd.read_csv('data/csv/Merged-2015.csv')
census2015 = (pd.read_csv('data/csv/census2015.csv', skiprows=1)).drop(["Id", "Id2"], axis=1)
census2016 = (pd.read_csv('data/csv/census2016.csv', skiprows=1)).drop(["Id", "Id2"], axis=1)
census2017 = (pd.read_csv('data/csv/census2017.csv', skiprows=1)).drop(["Id", "Id2"], axis=1)

# define map from county code to full name
# countyTranslations = {
#      'MN':'Manhattan',
#      'NY':'Manhattan',
#      'Q':'Queens',
#      'QN':'Queens',
#      'R':'Staten Island',
#      'ST':'Staten Island',
#      'K':'Brooklyn',
#      'BK': 'Brooklyn',
#      'BX':'Bronx',
#      'nan':'null'
# }

merged2015 = pd.DataFrame(merged2015, columns=['POSTCODE'])  # consider only the violation county column
merged2015 = merged2015.groupby('POSTCODE')['POSTCODE'].count().reset_index(name='count')  # group by violation county, count unique, add count column
merged2015["POSTCODE"] = merged2015["POSTCODE"].map(lambda x: str(x)[:5])

census2015["Geography"] = census2015["Geography"].map(lambda x: x.split(" ")[1])
census2015["Geography"] = census2015.merge(merged2015, how='right', left_on='Geography', right_on='POSTCODE')
census2015 = census2015.dropna(axis=0, how='any')
census2015 = census2015[census2015.columns[~census2015.columns.str.contains("error", flags=re.IGNORECASE)]]
census2015 = cleanCols(census2015)
census2015 = census2015.reindex(sorted(census2015.columns), axis=1)
census2015.reset_index()

for i, name in enumerate(list(census2015.drop("Geography", axis=1).columns)):
    print(i+1, name)

while 1:
    index = input("\nSelect Index of Statistic\n")
    try:
        index = int(index)
    except ValueError:
        print("Please Enter Index")
        continue
    if index > 38:
        print("Value to Big")
        continue
    break

index -= 1

for i, val in enumerate(list(census2015.iloc[:, index])):
    try:
        float(val)
    except ValueError:
        census2015 = census2015.drop(index=i)

colVals = census2015.iloc[:, index].map(lambda x: float(x))

mathFrame = pd.DataFrame()
mathFrame["Data"] = colVals
mathFrame["ZIP"] = census2015["Geography"]
mathFrame = mathFrame.sort_values(by="Data")
print(census2015.columns[index], "\n")
print(mathFrame)
print("Avg", round(colVals.sum() / (len(colVals)), 2))




