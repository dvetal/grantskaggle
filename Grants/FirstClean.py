# -*- coding: utf-8 -*-
"""
Created on Tue Sep  2 11:26:12 2014

@author: francesco


this script load raw.csv and removes the NaN valuesin 
the grants part of the table. From column 1 to 26.
Saves the result in clean.csv 

"""

import pandas as pd
#import numpy as np

grants = pd.read_csv('/home/francesco/Dropbox/DSR/5Week/raw.csv')

clean = grants[pd.isnull(grants['RFCD.Code.1'])==False]
clean = clean[pd.isnull(clean['SEO.Code.1'])==False]


clean.to_csv('clean.csv', index=False)

