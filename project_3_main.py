import pandas as pd


df = pd.read_csv('data/csv/ParkingViolations2015-Partial.csv', nrows=10000)

census2015 = (pd.read_csv('data/csv/census2015.csv', skiprows=1)).drop(["Id", "Id2"], axis=1)
census2016 = (pd.read_csv('data/csv/census2015.csv', skiprows=1)).drop(["Id", "Id2"], axis=1)
census2017 = (pd.read_csv('data/csv/census2015.csv', skiprows=1)).drop(["Id", "Id2"], axis=1)


columnHeaders = list(df.columns.values)
print(columnHeaders)

countyList = []
valueDictionary = {}
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

for index, row in df.iterrows():
     county = row["Violation County"]
     
     if county not in countyList:
          if not isinstance(county, str):
               countyList.append(str(county))
          else:
               countyList.append(county)
                        
     if county not in valueDictionary:
          valueDictionary[str(county)] = 1;
     else:
          currentValue = valueDictionary[str(county)];
          valueDictionary[str(county)] = currentValue + 1;

print("RESULTS:");
for key in valueDictionary:
     print(key, ": ", valueDictionary[key])

#print('##############')
#for key in countyTranslations:
 #    print(key, ": ", countyTranslations[key])
combinedValuesDictionary = {}

print("PROCESSING/COMBINING RESULTS....")
for key in valueDictionary:
     #if countyTranslations[key] != 'nan':
     included = False;
     for key2 in valueDictionary:
         # print(key2)
          #print(countyTranslations[key2])
          
          if countyTranslations[key] == countyTranslations[key2]:
               if key != key2:
                    #true duplicate
                    trueValue = valueDictionary[key] + valueDictionary[key2]
                    combinedValuesDictionary[countyTranslations[key]] = trueValue
                    included = True
               #combinedValuesDictionary[key] = trueValue; 
               
               #flag duplicate and add to results dictionary with the countryTranslations[key] as the key
               print("duplicate found")
                         #combine
                              
     if not included:
          combinedValuesDictionary[countyTranslations[key]] = valueDictionary[key]
                         

print("COMBINED/PROCESSED VALUES:");
for key in combinedValuesDictionary:
     print(key, ": ", combinedValuesDictionary[key])

countyCheck: int = 0
for index, row in census2015.iterrows():
   # for key in countyTranslations:
   #      print(row["Geography"].split("County")[0])
   #      print(countyTranslations[key])
   #      print(row["Geography"].split("County")[0] == countyTranslations[key])
   #      if row["Geography"].split("County")[0] in countyTranslations[key]:
   #          print(row["Geography"].split("County")[0])
   #          print(countyTranslations[key])
   #          print(row["Geography"].split("County")[0] in countyTranslations[key])
   #          countyCheck = 1
   #
   # if countyCheck == 0:
   #      census2015 = census2015[census2015.Geography != row["Geography"]]
   #      countyCheck = 0
   # else:
   census2015.Geography = census2015.Geography.replace(to_replace=row["Geography"], value=row["Geography"].split("County")[0])
print(census2015)
#for row in df.itertuples(index=True, name='Pandas'):
 #    getattr(row, "Registration State") 
  #   county = getattr(row, "Violation County")
   #  print(county)
    
    
    
    
    
    




