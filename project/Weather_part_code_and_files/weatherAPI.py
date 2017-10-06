# This file implements API to scrape weather data from NOAA (National Oceanic and Atmospheric Administration)
# Then form data into dataframe and merge data in the way we want to present

import requests
import pandas as pd
def getWeatherDat():
    locList = list()
    # Location at national arboretum
    locList.append('USC00186350')
    # Location at dalecavlia reservior
    locList.append('USC00182325')
    # location at Alexandra, VA. This station only contains PRCP and SNOW, no temperature data
    locList.append('US1VAFX0063')
    # Since the limit of results returned is 1000, we want to keep the each search 
    # period to 3 months so that the results won't exceed the limit
    dateList = list()
    yr = list()
    yr.append('2013')
    yr.append('2014')
    yr.append('2015')
    yr.append('2016')
    for i in range(len(yr)):
        dateList.append('startdate='+yr[i]+'-01-01&enddate='+yr[i]+'-03-31')
        dateList.append('startdate='+yr[i]+'-04-01&enddate='+yr[i]+'-06-30')
        dateList.append('startdate='+yr[i]+'-07-01&enddate='+yr[i]+'-09-30')
        dateList.append('startdate='+yr[i]+'-10-01&enddate='+yr[i]+'-12-31')    
    
    # a new data frame to store data from API
    df = pd.DataFrame()
    for i in range(len(dateList)):
        for k in range(len(locList)):
            BaseURL='https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&limit=1000&stationid=GHCND:'+locList[k]+'&units=standard&'+dateList[i]
            URLPost ={'token':'ekzgryaLzmqpLvYuHCERiUvLLGthmyJk'}
            response=requests.get(BaseURL,headers =URLPost)
            jsontxt = response.json()
            
            # For each result, it contains date, data type such as PRCP, SNOW, TMIN...
            # and its value 
            if (len(jsontxt) !=0):
                for j in range(len(jsontxt['results'])):
                    date = jsontxt['results'][j]['date']
                    value = jsontxt['results'][j]['value']
                    datType = jsontxt['results'][j]['datatype']
                    val = {'Date': [date],'Value':[str(value)],'DataType':[datType],'Location':[locList[k]]}
                    dat = pd.DataFrame.from_dict(val)
                    df = pd.concat([df,dat])
    return(df)
        
df = pd.DataFrame()
df = getWeatherDat()
# Store the data scraped using API into files 
df.to_csv('weatherOri.txt',sep = '|', index = False)
df.to_csv('weatherOri.csv',sep = ',', index = False)

# Codes below aims to merge the original data frame. The original data frame
# only contains column: date, data type and value. We want to merge the data by 
# date an location
df = pd.read_csv('weatherOri.csv' , sep=',', encoding='latin1')
# columns of the new data frame
col = pd.unique(df[df.columns[0]]).tolist()
col.append('Location')
col.append('Date')
dfNew = pd.DataFrame(columns = col)

# subset the big dataframe into 3 small ones based on the location
dfLocUSC00186350 = df[df['Location'] == 'USC00186350']
# sort the subset by date 
dfLocUSC00186350 =dfLocUSC00186350.sort_values(by=['Date'])
# Find number of unique dates and loop through the data by date
len(pd.unique(dfLocUSC00186350['Date']))
dateList = pd.unique(dfLocUSC00186350['Date']).tolist()
for i in range(len(dateList)):
    date = dateList[i]
    dfAtDate = dfLocUSC00186350[dfLocUSC00186350['Date']==date]
    datType = pd.unique(dfAtDate['DataType']).tolist()
    dat = {'Date':[date], 'Location': ['USC00186350']}
    # get data type and its value for that particular date and put them into 
    # one row
    for j in range(len(datType)):
        dat.update({datType[j]:[dfAtDate[dfAtDate['DataType'] ==datType[j]].iloc[0]['Value']]})
    dat = pd.DataFrame.from_dict(dat)
    dfNew = pd.concat([dfNew,dat])

# Same for location at dalecavlia reservior
dfLocUSC00182325 = df[df['Location'] == 'USC00182325']
# sort  the subset by date 
dfLocUSC00182325 =dfLocUSC00182325.sort_values(by=['Date'])
# Find number of unique dates and loop through the data by date
len(pd.unique(dfLocUSC00182325['Date']))
dateList = pd.unique(dfLocUSC00182325['Date']).tolist()
for i in range(len(dateList)):
    date = dateList[i]
    dfAtDate = dfLocUSC00182325[dfLocUSC00182325['Date']==date]
    datType = pd.unique(dfAtDate['DataType']).tolist()
    dat = {'Date':[date], 'Location': ['USC00182325']}
    # get data type and its value for that particular date and put them into 
    # one row
    for j in range(len(datType)):
        dat.update({datType[j]:[dfAtDate[dfAtDate['DataType'] ==datType[j]].iloc[0]['Value']]})
    dat = pd.DataFrame.from_dict(dat)
    dfNew = pd.concat([dfNew,dat])

# Same for location at Alexandra, VA
dfLocUS1VAFX0063 = df[df['Location'] == 'US1VAFX0063']
# sort  the subset by date 
dfLocUS1VAFX0063 =dfLocUS1VAFX0063.sort_values(by=['Date'])
len(pd.unique(dfLocUS1VAFX0063['Date']))
dateList = pd.unique(dfLocUS1VAFX0063['Date']).tolist()
for i in range(len(dateList)):
    date = dateList[i]
    dfAtDate = dfLocUS1VAFX0063[dfLocUS1VAFX0063['Date']==date]
    datType = pd.unique(dfAtDate['DataType']).tolist()
    dat = {'Date':[date], 'Location': ['US1VAFX0063']}
    for j in range(len(datType)):
        dat.update({datType[j]:[dfAtDate[dfAtDate['DataType'] ==datType[j]].iloc[0]['Value']]})
    dat = pd.DataFrame.from_dict(dat)
    dfNew = pd.concat([dfNew,dat])

# We only want PRCP, SNOW, TMIN and TMAX
# Delete all noise attributes 
del dfNew['DAPR']
del dfNew['MDPR']
del dfNew['SNWD']
del dfNew['TOBS']
del dfNew['WESD']
del dfNew['WESF']
del dfNew['WT01']
del dfNew['WT03']
del dfNew['WT04']
del dfNew['WT06']
del dfNew['WT11']

# Save the new merged data to file
dfNew.to_csv('weatherAfterMerge.txt',sep = '|', index = False)
dfNew.to_csv('weatherAfterMerge.csv',sep = ',', index = False)

            


