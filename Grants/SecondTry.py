# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 17:10:48 2014

@author: francesco
"""
import pandas as pd
import numpy as np

ready = pd.read_csv('/home/francesco/Dropbox/DSR/5Week/grantskaggle/Grants/MLready.csv')

complete = pd.DataFrame()

## creating grantid column
grantid = pd.Series(ready['GrantId'].values).unique()
grantid = pd.Series(grantid).apply(int)

complete['grantid'] = grantid
complete = complete.set_index(grantid)

toappend = []
toappend.append(grantid)
## creating teamsize column
teamsize = ready['teamSize'].groupby(ready['GrantId']).first()
complete['teamsize'] = teamsize


## creating publications columns
pubastar = ready['A*'].groupby(ready['GrantId']).sum()/teamsize
puba = ready['A'].groupby(ready['GrantId']).sum()/teamsize
pubb = ready['B'].groupby(ready['GrantId']).sum()/teamsize
pubc = ready['C'].groupby(ready['GrantId']).sum()/teamsize

complete['pubastar'] = pubastar
complete['puba'] = puba
complete['pubb'] = pubb
complete['pubc'] = pubc

## creating roles columns
temp = pd.concat([ready['GrantId'], pd.get_dummies(ready['Role'])], axis=1)
feat = temp.columns[1:]
roledummied = temp[feat].groupby(ready['GrantId']).sum()
complete = pd.concat([complete, roledummied], axis=1)

## creating year of birth columns
temp = pd.concat([ready['GrantId'], pd.get_dummies(ready['YearofBirth'])], axis=1)
feat = temp.columns[1:]
yearsdummied = temp[feat].groupby(ready['GrantId']).sum()
complete = pd.concat([complete, yearsdummied], axis=1)

## creating years of exp columns
temp = pd.concat([ready['GrantId'], pd.get_dummies(ready['NoofYearsinUniatTimeofGrant'])], axis=1)
feat = temp.columns[1:]
expdummied = temp[feat].groupby(ready['GrantId']).sum()
complete = pd.concat([complete, expdummied], axis=1)

## converting WithPhd = Yes to 1 and No to 0
ready.WithPHD[ready['WithPHD'] == 'Yes'] = 1
ready.WithPHD[ready['WithPHD'] == 'No'] = 0
phd = ready['WithPHD'].groupby(ready['GrantId']).sum()/teamsize
complete['phd'] = phd

## creating success grants
ready['totalSuccess'] = ready.NumberofSuccessfulGrant + ready.NumberofUnsuccessfulGrant
tot = ready['totalSuccess'].groupby(ready['GrantId']).sum()
grantsuccess = ready['NumberofSuccessfulGrant'].groupby(ready['GrantId']).sum()/tot
grantsuccess[pd.isnull(grantsuccess) == True] = 0
complete['grantsuccess'] = grantsuccess 

complete.to_csv('complete.csv', index = False)



