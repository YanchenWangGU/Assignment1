# This part tests how clean each attribute in the car crash dataset is
import pandas as pd
import time

df = pd.read_csv('originalCrash.csv' , sep=',', encoding='latin1')

## Get level of cleanliness of each variable 
# check for NaN data
NaCount = {}
for col in df.columns:
    NaCount[col] = df[col].isnull().values.ravel().sum()

# print(NaCount)
#{'ADDRESS': 28, 'BICYCLISTSIMPAIRED': 0, 'DRIVERSIMPAIRED': 0, 'FATAL_BICYCLIST': 0, 
# 'FATAL_DRIVER': 0, 'FATAL_PEDESTRIAN': 0, 'FROMDATE': 0, 'LATITUDE': 0, 'LONGITUDE': 0,
# 'MAJORINJURIES_BICYCLIST': 0, 'MAJORINJURIES_DRIVER': 0, 'MAJORINJURIES_PEDESTRIAN': 0,
# 'MINORINJURIES_BICYCLIST': 0, 'MINORINJURIES_DRIVER': 0, 'MINORINJURIES_PEDESTRIAN': 0,
# 'PEDESTRIANSIMPAIRED': 0, 'REPORTDATE': 0, 'SPEEDING_INVOLVED': 0, 'TOTAL_BICYCLES': 0,
# 'TOTAL_GOVERNMENT': 0, 'TOTAL_PEDESTRIANS': 0, 'TOTAL_TAXIS': 0, 'TOTAL_VEHICLES': 0,
# 'UNKNOWNINJURIES_BICYCLIST': 0, 'UNKNOWNINJURIES_DRIVER': 0, 'UNKNOWNINJURIES_PEDESTRIAN': 0}

fracNa = {}
for i in NaCount:
    fracNa[i] = NaCount[i]/len(df.index)

# print(fracNa)
# {'ADDRESS': 0.00029825308904985089, 'BICYCLISTSIMPAIRED': 0.0, 'DRIVERSIMPAIRED': 0.0,
# 'FATAL_BICYCLIST': 0.0, 'FATAL_DRIVER': 0.0, 'FATAL_PEDESTRIAN': 0.0, 'FROMDATE': 0.0,
# 'LATITUDE': 0.0, 'LONGITUDE': 0.0, 'MAJORINJURIES_BICYCLIST': 0.0, 'MAJORINJURIES_DRIVER': 0.0,
# 'MAJORINJURIES_PEDESTRIAN': 0.0, 'MINORINJURIES_BICYCLIST': 0.0, 'MINORINJURIES_DRIVER': 0.0,
# 'MINORINJURIES_PEDESTRIAN': 0.0, 'PEDESTRIANSIMPAIRED': 0.0, 'REPORTDATE': 0.0,
# 'SPEEDING_INVOLVED': 0.0, 'TOTAL_BICYCLES': 0.0, 'TOTAL_GOVERNMENT': 0.0,
# 'TOTAL_PEDESTRIANS': 0.0, 'TOTAL_TAXIS': 0.0, 'TOTAL_VEHICLES': 0.0, 'UNKNOWNINJURIES_BICYCLIST': 0.0,
# 'UNKNOWNINJURIES_DRIVER': 0.0, 'UNKNOWNINJURIES_PEDESTRIAN': 0.0}
# The date rarely has missing values. Addess is the only attribute has missing values
# and only .003% is missing

# check for noise values
noiseDat = {}
# Check for variable ADDRESS. If the address is all digits or the length of the 
# address is <=6 then it's highly likely to be wrong data
# However, some of the address entries only contain highway such as I295. We consider
# those are not noise. Hwy is the list of all highways in DC
def getNoiseAddress(df):
    count = 0
    Hwy = {'66','395','695','295'}
    for i in range(len(df.index)):
        if (df['ADDRESS'].iloc[i] is not None):
            # check if the address is a highway
            if (any(hwy in str(df['ADDRESS'].iloc[i]) for hwy in Hwy)):
                continue
            # if address is not all digit or length <=6
            if(not type(df['ADDRESS'].iloc[i]) ==str or 
               df['ADDRESS'].iloc[i].isdigit() or len(df['ADDRESS'].iloc[i])<=6):            
                count = count +1
    return(count)
count = getNoiseAddress(df)
noiseDat['ADDRESS'] = count



# Check for variable REPORTDATE and FROMDATE. Fromdate is the date of accident 
# and report date is the date that the accident is reported. We expect that 
# report date is latter than the from date
def getNoiseDate(df):
    count = 0
    for i in range(len(df.index)):
        fromDate = df['FROMDATE'].iloc[i].split('T')[0]
        reportDate = df['REPORTDATE'].iloc[i].split('T')[0]
        fromDate = time.strptime(fromDate, "%Y-%m-%d")
        reportDate = time.strptime(reportDate, "%Y-%m-%d")
        if(fromDate>reportDate):
            count = count+1
    return(count)
    
count = getNoiseDate(df)
noiseDat['FROMDATE'] = count
noiseDat['REPORTDATE'] = count

# print(len(df[df['BICYCLISTSIMPAIRED']!=0]))
# 7
# There are 7 impaired cyclist 
# Check for variable BICYCLISTSIMPAIRED. It is so extremely unlikely to have an 
# impaired cyclist that we don't really want put them into the study and we consider 
# all entries with non zero are noise values
noiseDat['BICYCLISTSIMPAIRED'] = len(df[df['BICYCLISTSIMPAIRED']!=0])

# Same for PEDESTRIANSIMPAIRED
# len(df[df['PEDESTRIANSIMPAIRED']!=0])
# 47
# Sincer there're only 47 acciednts that impaired pedestrains are involved and we 
# want to investgate relationship between weather and accident. So we consider that 
# 47 entries as noise values 

noiseDat['PEDESTRIANSIMPAIRED'] = len(df[df['PEDESTRIANSIMPAIRED']!=0])

# Check for UNKNOWNINJURIES_BICYCLIST, UNKNOWNINJURIES_DRIVER and UNKNOWNINJURIES_PEDESTRIAN
# we expect that the three attributes all have zero in them. Otherwise, they are 
# considered as noise
noiseDat['UNKNOWNINJURIES_BICYCLIST'] = len(df[df['UNKNOWNINJURIES_BICYCLIST']==1])
noiseDat['UNKNOWNINJURIES_DRIVER'] = len(df[df['UNKNOWNINJURIES_DRIVER']==1])
noiseDat['UNKNOWNINJURIES_PEDESTRIAN'] = len(df[df['UNKNOWNINJURIES_PEDESTRIAN']==1])

# Then we check MAJORINJURIES_BICYCLIST,MINORINJURIES_BICYCLIST and FATAL_BICYCLIST
# print(pd.unique(df['MAJORINJURIES_BICYCLIST']))
# [0 1]
# print(pd.unique(df['MINORINJURIES_BICYCLIST']))
# [0 1 2]
# print(pd.unique(df['FATAL_BICYCLIST']))
# [0 1]
# From the unique values, all three variables have reasonale values. So we want to check further
# Since TOTAL_BICYCLES is porvided in the data so we except to see number of major,minior 
# injuries and fatalities <= number of bicycles
def getNoiseCyc(df):
    count = 0
    for i in range(len(df.index)):
        sumInjuries = df['MAJORINJURIES_BICYCLIST'].iloc[i]+df['MINORINJURIES_BICYCLIST'].iloc[i]
        +df['FATAL_BICYCLIST'].iloc[i]+df['UNKNOWNINJURIES_BICYCLIST'].iloc[i]
        if (sumInjuries > df['TOTAL_BICYCLES'].iloc[i]):
            count = count +1
    return(count)
    
count = getNoiseCyc(df)
noiseDat['MAJORINJURIES_BICYCLIST'] = count
noiseDat['MINORINJURIES_BICYCLIST'] = count
noiseDat['FATAL_BICYCLIST'] = count
noiseDat['TOTAL_BICYCLES']=count

# Same strategy with driver, find sum of major, minior injuries and fatalities 
# and see if that number <= number of vehicles in the accident
def getNoiseDriver(df):
    count = 0
    for i in range(len(df.index)):
        sumInjuries = df['MAJORINJURIES_DRIVER'].iloc[i]+df['MINORINJURIES_DRIVER'].iloc[i]
        +df['FATAL_DRIVER'].iloc[i]++df['UNKNOWNINJURIES_DRIVER'].iloc[i]
        if (sumInjuries > df['TOTAL_VEHICLES'].iloc[i]):
            count = count +1
    return(count)
count = getNoiseDriver(df)
noiseDat['MAJORINJURIES_DRIVER'] = count
noiseDat['MINORINJURIES_DRIVER'] = count
noiseDat['FATAL_DRIVER'] = count

# Check for lat and long. The boundary of DC is lat:38.9955 to 38.79 Long: -77.12 to -76.90
def getNoiseLatLong(df):
    countLat = 0
    countLong = 0
    latNorth = 38.9955
    latSouth = 38.79
    longWest = -77.12
    longEast = -76.9
    for i in range(len(df.index)):
        if (df['LATITUDE'].iloc[i] > latNorth or df['LATITUDE'].iloc[i]<latSouth):
            countLat = countLat+1
        if (df['LONGITUDE'].iloc[i]<longWest or df['LONGITUDE'].iloc[i]>longEast):
            countLong = countLong+1
    return([countLat,countLong])
        
count = getNoiseLatLong(df)
noiseDat['LATITUDE'] = count[0]
noiseDat['LONGITUDE'] = count[1]

# Check for noise values in TOTAL_VEHICLES
# Since this is dataset for car accidents, TOTAL_VEHICLES = 0 is noise value
def getNoiseTotVeh(df):
    count = 0
    for i in range(len(df.index)):
        if (df['TOTAL_VEHICLES'].iloc[i]==0):
            count = count +1
    return(count)
            
count = getNoiseTotVeh(df)
noiseDat['TOTAL_VEHICLES'] =count

# Check if sum of major, minior injuries, fatalities and unknowns <= number of 
# pedestrians in the accident. If not then that record would be a noise value
def getNoisePed(df):
    count = 0
    for i in range(len(df.index)):
        sumInjuries = df['MAJORINJURIES_PEDESTRIAN'].iloc[i]+df['MINORINJURIES_PEDESTRIAN'].iloc[i]
        +df['FATAL_PEDESTRIAN'].iloc[i] +df['UNKNOWNINJURIES_PEDESTRIAN'].iloc[i]
        if (sumInjuries > df['TOTAL_PEDESTRIANS'].iloc[i]):
            count = count +1
    return(count)

count = getNoisePed(df)
noiseDat['MAJORINJURIES_PEDESTRIAN'] = count
noiseDat['MINORINJURIES_PEDESTRIAN'] = count
noiseDat['FATAL_PEDESTRIAN'] = count
noiseDat['TOTAL_PEDESTRIANS'] = count


# TOTAL_GOVERNMENT and TOTAL_TAXIS must be <= total vehicles in an accident
def getNoiseGovAndTaxi():
    count = 0
    for i in range(len(df.index)):
        sumVehicle = df['TOTAL_GOVERNMENT'].iloc[i] + df['TOTAL_TAXIS'].iloc[i]
        if (df['TOTAL_VEHICLES'].iloc[i] < sumVehicle):
            count = count +1
    return(count)

count = getNoiseGovAndTaxi()
noiseDat['TOTAL_GOVERNMENT'] = count
noiseDat['TOTAL_TAXIS'] = count

# SPEEDING_INVOLVED indicates if the reporting officer believed speeding was a 
# factor in the crash. This doesn't necessarily equate to participants being 
# ticketed/cited for speeding. However we still expect that number of SPEEDING_INVOLVED
# should not exceed number of vehicles.
# This attribute will be fixed in the next part into a categorical 0,1 attribute 
def getNoiseSpeeding(df):
    count = 0
    for i in range(len(df.index)):
        if (df['TOTAL_VEHICLES'].iloc[i] < df['SPEEDING_INVOLVED'].iloc[i]):
            count = count +1
    return(count)

count = getNoiseSpeeding(df)
noiseDat['SPEEDING_INVOLVED'] = count


# print(noiseDat)
# noiseDat:{'ADDRESS': 58,'BICYCLISTSIMPAIRED': 7, 'FATAL_BICYCLIST': 0, 'FATAL_DRIVER': 16,
# 'FATAL_PEDESTRIAN': 669, 'FROMDATE': 16598, 'LATITUDE': 0, 'LONGITUDE': 1, MAJORINJURIES_BICYCLIST': 0,
# 'MAJORINJURIES_DRIVER': 16,'MAJORINJURIES_PEDESTRIAN': 669,'MINORINJURIES_BICYCLIST': 0,'MINORINJURIES_DRIVER': 16,
# 'MINORINJURIES_PEDESTRIAN': 669,'PEDESTRIANSIMPAIRED': 27,'REPORTDATE': 16598,'SPEEDING_INVOLVED': 296,
# 'TOTAL_BICYCLES': 0,'TOTAL_GOVERNMENT': 5,'TOTAL_PEDESTRIANS': 669,'TOTAL_TAXIS': 5,
# 'TOTAL_VEHICLES': 295,'UNKNOWNINJURIES_BICYCLIST': 0,'UNKNOWNINJURIES_DRIVER': 0,'UNKNOWNINJURIES_PEDESTRIAN': 0}

# Get quality Score 
fracNoise = {}
for i in noiseDat:
    fracNoise[i] = noiseDat[i]/len(df.index)


# print(fracNoise)
# {'ADDRESS': 0.0006178099701746911, 'FROMDATE': 0.1768001704303366, 'REPORTDATE': 0.1768001704303366,
# 'BICYCLISTSIMPAIRED': 7.456327226246272e-05, 'PEDESTRIANSIMPAIRED': 0.0002876011930123562,
# 'MAJORINJURIES_BICYCLIST': 0.0, 'MINORINJURIES_BICYCLIST': 0.0, 'FATAL_BICYCLIST': 0.0,
# 'TOTAL_BICYCLES': 0.0, 'MAJORINJURIES_DRIVER': 0.00017043033659991478, 
# 'MINORINJURIES_DRIVER': 0.00017043033659991478, 'FATAL_DRIVER': 0.00017043033659991478,
# 'LATITUDE': 0.0, 'LONGITUDE': 1.0651896037494674e-05, 'TOTAL_VEHICLES': 0.003142309331060929,
# 'MAJORINJURIES_PEDESTRIAN': 0.007126118449083937, 'MINORINJURIES_PEDESTRIAN': 0.007126118449083937,
# 'FATAL_PEDESTRIAN': 0.007126118449083937, 'TOTAL_PEDESTRIANS': 0.007126118449083937,
# 'TOTAL_GOVERNMENT': 5.325948018747337e-05, 'TOTAL_TAXIS': 5.325948018747337e-05,
# 'SPEEDING_INVOLVED': 0.0031529612270984235, 'UNKNOWNINJURIES_BICYCLIST': 0.0,
# 'UNKNOWNINJURIES_DRIVER': 0.0, 'UNKNOWNINJURIES_PEDESTRIAN': 0.0}
    
# This dataset contains more noise values than missing values. REPORTDATE and FROMDATE
# have the most noise values. In the study, we may need to drop them because they 
# are very likely to be incorrect because report date can't be earlier than the 
# date of accident 



