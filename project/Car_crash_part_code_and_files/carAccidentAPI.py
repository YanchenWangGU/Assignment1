import requests
import pandas as pd

def getCrashAPI():
    BaseURL = "https://opendata.arcgis.com/datasets/70392a096a8e431381f1f692aaa06afd_24.geojson"
    response=requests.get(BaseURL)
    df = pd.DataFrame()
    jsontxt = response.json()
    # my_list is a list to record the indices of accidents that report date and 
    # from date are between 2013 and 2016
    my_list = list()
    # values is all years we want to include 
    values = {'2013','2014','2015','2016'}
    
    for i in range(len(jsontxt['features'])):
        FromYr = jsontxt['features'][i]['properties']['FROMDATE']
        ReportYr = jsontxt['features'][i]['properties']['REPORTDATE']
        # Since all dates have format yyyy-mm-ddT+time' then the year of that date
        # is the first 4 digits before '-' 
        if (FromYr is not None and ReportYr is not None):
            # if both from date and report date are both between 2013 and 2016 then
            # recoed the indeices for the row into my_list
            if (FromYr.split("-")[0] in values and ReportYr.split("-")[0] in values):
                my_list.append(i)   
    # define the attributes from the data set
    for i in my_list:
        FROMDATE = jsontxt['features'][i]['properties']['FROMDATE']
        REPORTDATE = jsontxt['features'][i]['properties']['REPORTDATE']
        ADDRESS = jsontxt['features'][i]['properties']['ADDRESS']
        LATITUDE = jsontxt['features'][i]['properties']['LATITUDE']
        LONGITUDE = jsontxt['features'][i]['properties']['LONGITUDE']
        MAJORINJURIES_BICYCLIST = jsontxt['features'][i]['properties']['MAJORINJURIES_BICYCLIST']
        MINORINJURIES_BICYCLIST = jsontxt['features'][i]['properties']['MINORINJURIES_BICYCLIST']
        UNKNOWNINJURIES_BICYCLIST = jsontxt['features'][i]['properties']['UNKNOWNINJURIES_BICYCLIST']
        FATAL_BICYCLIST = jsontxt['features'][i]['properties']['FATAL_BICYCLIST']
        MAJORINJURIES_DRIVER = jsontxt['features'][i]['properties']['MAJORINJURIES_DRIVER']
        MINORINJURIES_DRIVER = jsontxt['features'][i]['properties']['MINORINJURIES_DRIVER']
        UNKNOWNINJURIES_DRIVER = jsontxt['features'][i]['properties']['UNKNOWNINJURIES_DRIVER']
        FATAL_DRIVER = jsontxt['features'][i]['properties']['FATAL_DRIVER']
        MAJORINJURIES_PEDESTRIAN = jsontxt['features'][i]['properties']['MAJORINJURIES_PEDESTRIAN']
        MINORINJURIES_PEDESTRIAN = jsontxt['features'][i]['properties']['MINORINJURIES_PEDESTRIAN']
        UNKNOWNINJURIES_PEDESTRIAN = jsontxt['features'][i]['properties']['UNKNOWNINJURIES_PEDESTRIAN']
        FATAL_PEDESTRIAN = jsontxt['features'][i]['properties']['FATAL_PEDESTRIAN']
        TOTAL_VEHICLES = jsontxt['features'][i]['properties']['TOTAL_VEHICLES']
        TOTAL_BICYCLES = jsontxt['features'][i]['properties']['TOTAL_BICYCLES']
        TOTAL_PEDESTRIANS = jsontxt['features'][i]['properties']['TOTAL_PEDESTRIANS']
        PEDESTRIANSIMPAIRED = jsontxt['features'][i]['properties']['PEDESTRIANSIMPAIRED']
        BICYCLISTSIMPAIRED = jsontxt['features'][i]['properties']['BICYCLISTSIMPAIRED']
        DRIVERSIMPAIRED = jsontxt['features'][i]['properties']['DRIVERSIMPAIRED']
        TOTAL_TAXIS = jsontxt['features'][i]['properties']['TOTAL_TAXIS']
        TOTAL_GOVERNMENT = jsontxt['features'][i]['properties']['TOTAL_GOVERNMENT']
        SPEEDING_INVOLVED = jsontxt['features'][i]['properties']['SPEEDING_INVOLVED']
        
        # For each row/ record, form the values of each attribute into data frame
        # type and append it to the data frame to return
        dat = pd.DataFrame({'FROMDATE': [FROMDATE],'REPORTDATE':[REPORTDATE],
                            'ADDRESS':[ADDRESS],'LATITUDE':[LATITUDE],'LONGITUDE':[LONGITUDE],
                            'MAJORINJURIES_BICYCLIST':[MAJORINJURIES_BICYCLIST],'MINORINJURIES_BICYCLIST':[MINORINJURIES_BICYCLIST],
                            'UNKNOWNINJURIES_BICYCLIST':[UNKNOWNINJURIES_BICYCLIST],'FATAL_BICYCLIST':[FATAL_BICYCLIST],
                            'MAJORINJURIES_DRIVER':[MAJORINJURIES_DRIVER],'MINORINJURIES_DRIVER':[MINORINJURIES_DRIVER],
                            'UNKNOWNINJURIES_DRIVER':[UNKNOWNINJURIES_DRIVER],'FATAL_DRIVER':[FATAL_DRIVER],
                            'MAJORINJURIES_PEDESTRIAN':[MAJORINJURIES_PEDESTRIAN],'MINORINJURIES_PEDESTRIAN':[MINORINJURIES_PEDESTRIAN],
                            'UNKNOWNINJURIES_PEDESTRIAN':[UNKNOWNINJURIES_PEDESTRIAN],'FATAL_PEDESTRIAN':[FATAL_PEDESTRIAN],
                            'TOTAL_VEHICLES':[TOTAL_VEHICLES],'TOTAL_BICYCLES':[TOTAL_BICYCLES],'TOTAL_PEDESTRIANS':[TOTAL_PEDESTRIANS],
                            'PEDESTRIANSIMPAIRED':[PEDESTRIANSIMPAIRED],'BICYCLISTSIMPAIRED':[BICYCLISTSIMPAIRED],
                            'DRIVERSIMPAIRED':[DRIVERSIMPAIRED],'TOTAL_TAXIS':[TOTAL_TAXIS],
                            'TOTAL_GOVERNMENT':[TOTAL_GOVERNMENT],'SPEEDING_INVOLVED':[SPEEDING_INVOLVED]})
        # concat/ append dat to the df
        df = pd.concat([df,dat])
    return(df)

df = pd.DataFrame()
df = getCrashAPI()
# save the data set from API to files for future use
df.to_csv('originalCrash.txt',sep = '|', index = False)
df.to_csv('originalCrash.csv',sep = ',', index = False)