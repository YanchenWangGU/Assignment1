In the folder Car crash part code and files:

carAccidentAPI.py is python code to implement API to scrape car crash data from http://opendata.dc.gov/datasets/crashes-in-dc

originalCrash.csv and originalCrash.txt are the data files of car crash databy using API

carAccidentCleaning.py is python code to clean the attribute "SPEEDING_INVOLVED" to transform it into categorical (binary) data (either 0 or 1)

carAccidentCleanliness.py is python code to test how clean each attribute in the car crash dataset is

In the folder Weather part code and files:
weatherAPI.py is python code to implement API to scrape weather data from NOAA (National Oceanic and Atmospheric Administration)

weatherOri.csv is original data file obtained by using API.

WeatherCleaning.py is the python code that cleans two attributes in weather dataset

WeatherCleanliness.py is python code to test how clean each attribute in the weather dataset is

weatherAfterCleaning.csv is data file after cleaning the attributes "PRCP" and "SNOW"

weatherAfterMerge.csv is data file after merging items from the original dataset using API based on date and location

Outside the two folders:
ANLY501 Project Assignment1 contains all text for all questions 