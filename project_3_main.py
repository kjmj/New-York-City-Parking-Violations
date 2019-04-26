import pandas as pd
import math
import matplotlib.pyplot as plt
import mplleaflet

class Address:
     def __init__(self):
          self.number = 0
          self.street = ""
          self.addressRange = []
          



df = pd.read_csv('C:\\Users\\Noah Parker\\Documents\\Social_Imps_Data\\Year_2017.csv', nrows=100)
openmaps = pd.read_csv('C:\\Users\\Noah Parker\\Python_Repos\\New-York-City-Parking-Violations\\city_of_new_york.csv')
openmaps['NUMBER'] = pd.to_numeric(openmaps['NUMBER'], errors='coerce')

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

streetNameSuffix = ["th","nd"]

addressObjectList = []

for index, row in df.iterrows():
     county = row["Violation County"] 
     addressNumber = row["House Number"]
     addressStreet = row["Street Name"]
     address = Address()
     
     if isinstance(addressNumber, str):
          if "-" in addressNumber: #special case where street numbers are a range like 30-11
               array = addressNumber.split("-")
               address.addressRange = array
          elif addressNumber.isdigit(): #figure out entries with letters as street numbers...
               formattedNumber = int(addressNumber)
               if not math.isnan(formattedNumber):
                    address.number = formattedNumber
                    address.street = addressStreet
                    addressObjectList.append(address)
               
         
               
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

#Note: numbered streets are currently causing problems.
#i.e. 400 E 97th from the violation database won't get a result because in the
#address database it is 'E  97 ST'
#seems to follow the same pattern through: letter, 2 spaces, number.
for key in addressObjectList:
     number = int(key.number)
     street = key.street
     print(repr(number) + " "+ street)
     
     if len(key.addressRange) == 0:
          
          firstSearch = None
          #other case is if street name only contains one letter? i.e. E 97th St
          #this case covers both E  97th and 9th Ave -- still need to figure out conditional formatting
          #searchterms like 5  Ave are still broken
          
          if any(char.isdigit() for char in key.street):
               if "th" in key.street:
                    print("suffix found")
                    key.street = key.street.replace("th", "")
                    key.street = key.street.replace(" ", "  ", 1)
               if "nd" in key.street:
                    print("suffix found")
                    key.street = key.street.replace("nd", "")
                    key.street = key.street.replace(" ", "  ", 1)
               print("searchTerm: "+key.street)
               firstSearch = openmaps[(openmaps['STREET'].str.match(key.street, case=False))]
          else:
               print("Street name not a number")
               firstSearch = openmaps[(openmaps['STREET'].str.contains(street, case=False))]
          
          if not firstSearch.empty:
               search = firstSearch[(firstSearch['NUMBER'] == number)]
               
               #search = openmaps[(openmaps['STREET'].str.contains(street, case=False)) & (openmaps['NUMBER'] == number)]          
               
               #search = openmaps[(openmaps['STREET'].str.contains(street, case=False)) & (openmaps['NUMBER'].between(number - 10, number + 10, inclusive=False))]
               #exact = search[(search['NUMBER'] == number)]
               if search.empty:
                    #search through search for closest match
                    search = openmaps[(openmaps['STREET'].str.contains(street, case=False)) & (openmaps['NUMBER'].between(number - 10, number + 10, inclusive=False))]
                    closest = 10
             
                    closestRow = None
                    for index, row in search.iterrows():
                         if abs(row['NUMBER'] - number) < closest:
                              closestRow = row
                              closest = abs(row['NUMBER'] - number)
                         
                              closestLat = closestRow['LAT']
                              closestLong = closestRow['LON']
                              print("Closest Address Found")      
                              plot.plot(closestLong, closestLat, markersize=3, color='yellow')
               else:
                    entry = search.iloc[0]
                    lat = entry['LAT']
                    long = entry['LON']
                    print("EXACT:")
                    plt.plot(long, lat, marker='o', markersize=3, color="blue")
                    print(str(lat)+ ", "+str(long))
          else:
               print("firstSearch was empty")          
          #more than one address
          #for now do nothing but eventually will probably just change the .between call

mplleaflet.show()


#print("RESULTS:");
#for key in valueDictionary:
 #    print(key, ": ", valueDictionary[key])

#print('##############')
#for key in countyTranslations:
 #    print(key, ": ", countyTranslations[key])
#combinedValuesDictionary = {}

#print("PROCESSING/COMBINING RESULTS....")
#for key in valueDictionary:
     #if countyTranslations[key] != 'nan':
 #    included = False;
  #   for key2 in valueDictionary:
         # print(key2)
          #print(countyTranslations[key2])
          
   #       if countyTranslations[key] == countyTranslations[key2]:
    #           if key != key2:
      #              trueValue = valueDictionary[key] + valueDictionary[key2]
     #               combinedValuesDictionary[countyTranslations[key]] = trueValue
       #             included = True
               #combinedValuesDictionary[key] = trueValue; 
               
               #flag duplicate and add to results dictionary with the countryTranslations[key] as the key
        #       print("duplicate found")
                         #combine
                              
     #if not included:
     #     combinedValuesDictionary[countyTranslations[key]] = valueDictionary[key]
                         

#print("COMBINED/PROCESSED VALUES:");
#for key in combinedValuesDictionary:
 #    print(key, ": ", combinedValuesDictionary[key])
                         
#for row in df.itertuples(index=True, name='Pandas'):
 #    getattr(row, "Registration State") 
  #   county = getattr(row, "Violation County")
   #  print(county)
