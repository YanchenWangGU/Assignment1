# this file will test how clean each attribute in the weather dataset is
import pandas as pd

df = pd.read_csv('weatherAfterMerge.csv' , sep=',', encoding='latin1')
## test number of missing values for attributes PRCP, SNOW, 
## Tmax, Tmin(Tmax, Tmin are only for the first two locations)
missVal= {}
missVal['Date'] = df['Date'].isnull().values.ravel().sum()
missVal['PRCP'] = df['PRCP'].isnull().values.ravel().sum()
missVal['SNOW'] = df['SNOW'].isnull().values.ravel().sum()
missVal['TMIN'] = df[df['Location'] != 'US1VAFX0063']['TMIN'].isnull().values.ravel().sum()
missVal['TMAX'] = df[df['Location'] != 'US1VAFX0063']['TMIN'].isnull().values.ravel().sum()
## missVal:{'Date': 0, 'PRCP': 35, 'SNOW': 1524, 'TMAX': 24, 'TMIN': 24}

fracNa = {}
for i in missVal:
    fracNa[i] = missVal[i]/len(df.index)

# print(fracNa)
# fracNa:{'Date': 0.0, 'PRCP': 0.0085303436509870829, 'SNOW': 0.37143553497440895, 
# 'TMIN': 0.0058493785035339998, 'TMAX': 0.0058493785035339998}
# SNOW has the most missing values 

noiseVal = {}
## Check for noise values in Date. There are 365*3+366 = 1461 days in the four years 
## and we can see if the number of unique values == 1461
noiseVal['Date'] = len(pd.unique(df['Date'])) - 1461
# Check noise values in PRCE we define incorrect if the maximum - minimum for 
# that day is more than 1 because it is very unlikely to have more than 1 inch
# difference in raining
dateList = pd.unique(df['Date']).tolist()
def getNoisePRCP(df,dateList):
    count = 0
    for i in range(len(dateList)):
        date = dateList[i]
        if((max(df[df['Date']==date]['PRCP']) - min(df[df['Date']==date]['PRCP']))>1):
            count = count+1
    return(count)
            
count = getNoisePRCP(df,dateList)  
noiseVal['PRCP'] = count
    
    
# Same for SNOW that noise values are defined if maximum - minimum snowing for 
# that day is more than 2 inches
def getNoiseSNOW(df,dateList):
    count = 0
    for i in range(len(dateList)):
        date = dateList[i]
        if((max(df[df['Date']==date]['SNOW']) - min(df[df['Date']==date]['SNOW']))>2):
            count = count+1
    return(count)

count =getNoiseSNOW(df,dateList)
noiseVal['SNOW'] = count

# Check missing values in TMAX. We expect the temperature across different stations
# in DC to be about the same. So if difference in max temperature across stations is
# more than 10 degrees then it's likely to be incorrect 
def getNoiseTemp(df,dateList):
    countTempMin = 0
    countTempMax = 0
    for i in range(len(dateList)):
        date = dateList[i]
        if((max(df[df['Date']==date]['TMAX']) - min(df[df['Date']==date]['TMAX']))>10):
            countTempMax = countTempMax+1
        if((max(df[df['Date']==date]['TMIN']) - min(df[df['Date']==date]['TMIN']))>10):
            countTempMin = countTempMin+1
    return[countTempMin,countTempMax]

count = getNoiseTemp(df,dateList)
noiseVal['TMIN'] = count[0]
noiseVal['TMAX'] = count[1]

# noiseVal:{'Date': 0, 'PRCP': 21, 'SNOW': 6, 'TMAX': 47, 'TMIN': 29}

# Get fraction of noise values. Since the noise values are in days for example
# if maximum - minimum snowing for that day is too big then we define SNOW for 
# that day is a noise value
fracNoise = {}
for i in noiseVal:
    fracNoise[i] = noiseVal[i]/len(pd.unique(df['Date']))
    
# print(fracNoise)
# fracNoise:{'Date': 0.0, 'PRCP': 0.014373716632443531, 'SNOW': 0.004106776180698152,
# 'TMAX': 0.03216974674880219, 'TMIN': 0.019849418206707735}
# We can see that PRCP has the most noise values 