# This file cleans the attribute "SPEEDING_INVOLVED" to transform it into categorical (binary) data (either 0 or 1)
import pandas as pd
df = pd.read_csv('originalCrash.csv' , sep=',', encoding='latin1')

## From the description of the data, SPEEDING_INVOLVED indicates if the reporting 
## officer believed speeding was a factor in the crash. This doesn't necessarily 
## equate to participants being ticketed/cited for speeding. 
## In this case, it's reasonable to convert this attribute into a categorical attribute
## 0 means no speeding and 1 means speeding.
for i in range(len(df.index)):
    if (not df['SPEEDING_INVOLVED'].iloc[i] ==0):
        df['SPEEDING_INVOLVED'].iat[i] = 1

# Re-run and check if the quality improves 
count = 0
for i in range(len(df.index)):
    if (df['TOTAL_VEHICLES'].iloc[i] < df['SPEEDING_INVOLVED'].iloc[i]):
        count = count +1
# print(count)
# 0 
df.to_csv('crashAfterCleaning.csv',sep = ',', index = False)
