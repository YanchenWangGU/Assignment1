# This part cleans two attributes "PRCP" and "SNOW" in weather dataset
import pandas as pd
import numpy as np

## The codes below will fix missing values and noise values in attributes 
## "PRCP" and "SNOW'
dfNew = pd.read_csv('weatherAfterMerge.csv' , sep=',', encoding='latin1')
## Fix snow missing data. If minimum temp > 32 then it's impossible to have snow
snowNAList = dfNew[dfNew['SNOW'].isnull()].index.tolist()
for i in snowNAList:
    date = dfNew.iloc[i]['Date']
    if(any(dfNew[dfNew['Date']==date]['TMIN'] > 32)):
        dfNew.loc[i,'SNOW'] = 0
    
## see how it improves after replacing the missing values
# print(dfNew['SNOW'].isnull().values.ravel().sum())
# 257
# This step reduces missing data from about 1500 to 257
        
## Replace rest of the missing values by taking mean of the snow data for that day
## Update missing value list
snowNAList = dfNew[dfNew['SNOW'].isnull()].index.tolist()
for i in snowNAList:
    date = dfNew.iloc[i]['Date']
    # check if there is at least one non missing SNOW data for that day
    if(not all(val is None for val in dfNew[dfNew['Date']==date]['SNOW'])):
        mean = np.mean(dfNew[dfNew['Date']==date]['SNOW'])
        dfNew.loc[i,'SNOW'] = mean
# print(dfNew['SNOW'].isnull().values.ravel().sum())
# 3
# The missing value reduced from about 257 entries to 3 entries

## correct incorrect data in SNOW
dateList = pd.unique(dfNew['Date']).tolist()
for i in range(len(dateList)):
    date = dateList[i]
    # we define incorrect if the maximum - minimum for that day is more than 2
    # because it is very unlikely to have more than 2 inches difference of snowing
    # To fix it, we replace the value by taking mean for that day
    if((max(dfNew[dfNew['Date']==date]['SNOW']) - min(dfNew[dfNew['Date']==date]['SNOW']))>2):
        mean = np.mean(dfNew[dfNew['Date']==date]['SNOW'])
        dfNew.loc[dfNew['Date']==date,'SNOW'] = mean
        
## Rerun cleanliness and see how it improves 
count = 0
for i in range(len(dateList)):
    date = dateList[i]
    if((max(dfNew[dfNew['Date']==date]['SNOW']) - min(dfNew[dfNew['Date']==date]['SNOW']))>2):
        count = count+1
# print(count)
# 0 
# Number of incorrect values reduces to zero from 6
        
# After fixing missing and incorrect values, there are only 3 missing with no incorrect values

## Fix missing values in PRCP 
## Replace missing values using mean of PRCP for that day
PRCPNAList = dfNew[dfNew['PRCP'].isnull()].index.tolist()
for i in PRCPNAList:
    date = dfNew.iloc[i]['Date']
    # Same as SNOW, there must be at least one non missing for that day 
    if(not all(val is None for val in dfNew[dfNew['Date']==date]['PRCP'])):
        mean = np.mean(dfNew[dfNew['Date']==date]['PRCP'])
        dfNew.loc[i,'PRCP'] = mean
        
# print(dfNew['PRCP'].isnull().values.ravel().sum())
# 0
# Number of missing values reduces from 35 to 0
    
# Correct incorrect data in PRCP by taking mean PRCP for that day
dateList = pd.unique(dfNew['Date']).tolist()
for i in range(len(dateList)):
    date = dateList[i]
    # we define incorrect if the maximum - minimum for that day is more than 1
    # because it is very unlikely to have more than 1 inche difference in raining
    if((max(dfNew[dfNew['Date']==date]['PRCP']) - min(dfNew[dfNew['Date']==date]['PRCP']))>1):
        mean = np.mean(dfNew[dfNew['Date']==date]['PRCP'])
        dfNew.loc[dfNew['Date']==date,'PRCP'] = mean
        
# After cleaning, we check if there is any other incorrect values
count = 0
dateList = pd.unique(dfNew['Date']).tolist()
for i in range(len(dateList)):
    date = dateList[i]
    if((max(dfNew[dfNew['Date']==date]['PRCP']) - min(dfNew[dfNew['Date']==date]['PRCP']))>1):
        count = count+1
# print(count)
# 0
# There is no missing or incorrect values in PRCP after fixing 

# Save the cleaned dataset into files 
dfNew.to_csv('weatherAfterCleaning.csv',sep = ',', index = False)
