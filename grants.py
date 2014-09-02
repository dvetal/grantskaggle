
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  1 10:49:12 2014

@author: francesco
"""
import pandas as pd
import numpy as np

grants = pd.read_csv('/home/francesco/Dropbox/DSR/5Week/raw.csv')

columns = grants.columns
col = columns[26:]
a = columns[26:41].values
b = [ i.replace(".","") for i in a ] 
names = [ i[:-1] for i in b ] ## get rid of the number at the end of column name
names[-4] = names[-4] + '*'
names.insert(0,'GrantId')


def shapeGrantInv(row, col, names):
    import numpy as np
    import pandas as pd
    
    grantid = row[0]
    investigators = row[col]
    invIds = investigators[::15]
 
    n_Inv = invIds.count().sum()

    dataframe = pd.DataFrame(np.zeros((n_Inv, len(names))), columns = names)
    
    for i in range(n_Inv):
        dataframe.iloc[i,0] = grantid  
        jump = i*15
        dataframe.iloc[i,1:] = investigators[jump:jump+15].values
    
    return dataframe
    
vertical = pd.DataFrame(np.zeros((1, len(names))), columns = names)

for i in range(grants.shape[0]):
    data = shapeGrantInv(grants.iloc[i,:],col,names)
    vertical = vertical.append(data, ignore_index = True)

vertical = vertical[pd.isnull(vertical.PersonID)==False]
vertical = vertical[1:]    
vertical.to_csv('vertical.csv')
