# -*- coding: utf-8 -*-
"""
Created on Tue Sep  2 11:26:12 2014

@author: francesco

loads vertical.csv and cleans it, taking care of NaN, dropping meaningless features and 
adding TeamSize column

"""

import pandas as pd
import numpy as np

vertical = pd.read_csv('vertical.csv')

vertical['GrantId'] = vertical['GrantId'].apply(int) ## converting grantId to int 
vertical['PersonID'] = vertical['PersonID'].apply(int) ## converting PersonID to int
#pd.Series(vertical['GrantId'].values).unique()
vertical.iloc[749,2] = 'CHIEF_INVESTIGATOR' ## only onr NaN in Role column. Imputing it with CHIEF_INVESTIGATOR
vertical.WithPHD[vertical.WithPHD.isnull()] = 'No' ## imputing NaN in WithPHD with No
vertical.WithPHD = vertical.WithPHD.apply(lambda x: x.strip()) ## stripping white space after Yes 

vertical['A'] = vertical['A'].apply(int) ## converting to int
vertical['A*'] = vertical['A*'].apply(int) ## converting to int
vertical['C'] = vertical['C'].apply(int) ## converting to int
vertical['B'] = vertical['B'].apply(int) ## converting to int
vertical['NumberofSuccessfulGrant'] = vertical['NumberofSuccessfulGrant'].apply(int) ## converting to int
vertical['NumberofUnsuccessfulGrant'] = vertical['NumberofUnsuccessfulGrant'].apply(int) ## converting to int

## missing Year of Births are imputed with the median of the YoB of the persons with '>=0 to 5' 'NoofYearsinUniatTimeofGrant'
vertical.YearofBirth[vertical['YearofBirth'].isnull()] = vertical.YearofBirth[vertical['NoofYearsinUniatTimeofGrant'] == '>=0 to 5'].median() 

vertical['YearofBirth'] = vertical['YearofBirth'].apply(int) ## converting to int

## convert the category to min of time interval
vertical.NoofYearsinUniatTimeofGrant[vertical['NoofYearsinUniatTimeofGrant'] == 'Less than 0'] = 0 # years set to 0
vertical.NoofYearsinUniatTimeofGrant[vertical['NoofYearsinUniatTimeofGrant'] == '>=0 to 5'] = 0 # years set to 0
vertical.NoofYearsinUniatTimeofGrant[vertical['NoofYearsinUniatTimeofGrant'] == 'more than 15'] = 15 # years set to 15
vertical.NoofYearsinUniatTimeofGrant[vertical['NoofYearsinUniatTimeofGrant'] == '>10 to 15'] = 10 # years set to 10
vertical.NoofYearsinUniatTimeofGrant[vertical['NoofYearsinUniatTimeofGrant'] == '>5 to 10'] = 5 # years set to 5

## imputing the missing values of NoofYearsinUniatTimeofGrant with 0
vertical.NoofYearsinUniatTimeofGrant[vertical.NoofYearsinUniatTimeofGrant.isnull()] = 0


first4Columns = list(vertical.columns.values[:4])

for col in vertical.columns.values[8:]:
    first4Columns.append(col)
    
investigators = vertical[first4Columns] ## dropping the 3 columns about country, language etc

#### the following 5 lines of code create a new column called TeamSize
#### adding the number of persons for each Team
f = investigators.groupby(['GrantId']).size()
g = list(f) 
h = [[el]*el for el in g]
final = pd.Series([i for sub in h for i in sub])
investigators['teamSize'] = final

investigators.to_csv('investigators.csv', index=False)
