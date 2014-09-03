# -*- coding: utf-8 -*-
"""
Grant Kaggle Competition

Created on Wed Sep  2 9:38:00 2014

@author: Don Vetal
"""

import csv
import pandas as pd
import numpy as np
import os

os.chdir('PublicProjects/Grants')

raw = pd.read_csv('clean.csv')
rawGrants = raw.loc[:,'Grant.Application.ID':'SEO.Percentage.5']
rawGrants.columns = ['GrantApplicationID','GrantStatus','SponsorCode','GrantCategoryCode',
'ContractValueBand','Startdate','RFCDCode1','RFCDPercentage1','RFCDCode2','RFCDPercentage2',
'RFCDCode3','RFCDPercentage3','RFCDCode4','RFCDPercentage4','RFCDCode5','RFCDPercentage5',
'SEOCode1','SEOPercentage1','SEOCode2','SEOPercentage2','SEOCode3','SEOPercentage3',
'SEOCode4','SEOPercentage4','SEOCode5','SEOPercentage5']

rawGrants.to_csv('data/grantsRaw.csv')

##Below is DON's code for the making of the long table....use the other loaded file.
#Not used because we wanted to make sure we had a consistent file.

#rawInvest = raw.iloc[:,27:]
#rawInvest['Grant.Application.ID'] = raw['Grant.Application.ID']
#rawInvest = rawInvest.drop('X', 1)

#longInvest = pd.DataFrame()
#for i in range(0,15):
#	j = 15*i
#	temp = list(rawInvest.columns[(j):(j+15)])
#	temp.append(rawInvest.columns[225])
#	tempFrame = rawInvest[temp]
#	tempFrame.columns = ['PersonID','Role','YearofBirth','CountryofBirth',
#	'HomeLanguage','DeptNo','FacultyNo','WithPHD','NoYearsinUni',
#	'NumofSuccessfulGrant','NumofUnsuccessfulGrant','Astar','A','B','C',
#	'GrantApplicationID'] 
#	longInvest = pd.concat(objs = [longInvest, tempFrame], axis = 0)

#longInvest.to_csv('data/longtable.csv')
#rawGrants.to_csv('data/grants.csv')

# take a look at the unique values of some columns
# Simple exploration of the two csvs to check for NAs and categories.
longInvest = pd.read_csv('vertical.csv')

longInvest = longInvest.iloc[:,1:]

for k in longInvest.columns:
	print 'Column Name: ' + k
	print pd.Series(longInvest[k].values).unique()
	print '/n'
	print 'Number of Nulls (nan): ' + k
	print '# of Nulls: ' + str(longInvest[k].isnull().sum())

for m in rawGrants.columns:
	print 'Column Name: ' + m
	print pd.Series(rawGrants[m].values).unique()
	print ''
	print 'Number of Nulls (nan) for : ' + m
	print '# of Nulls: ' + str(rawGrants[m].isnull().sum())

### Do some Additional Munging ###

## Step 1: Strip the last 4 digits

# 1.1: Turn everthing I need to into a string
for k in rawGrants.iloc[:,6:].columns:
	rawGrants[k].astype(str)
# 1.2

for i in range(len(rawGrants)):
	rawGrants.RFCDCode1[i] = str(rawGrants.RFCDCode1[i])[0:2]
	rawGrants.RFCDCode2[i] = str(rawGrants.RFCDCode2[i])[0:2]
	rawGrants.RFCDCode3[i] = str(rawGrants.RFCDCode3[i])[0:2]
	rawGrants.RFCDCode4[i] = str(rawGrants.RFCDCode4[i])[0:2]
	rawGrants.RFCDCode5[i] = str(rawGrants.RFCDCode5[i])[0:2]
	rawGrants.SEOCode1[i] = str(rawGrants.SEOCode1[i])[0:2]
	rawGrants.SEOCode2[i] = str(rawGrants.SEOCode2[i])[0:2]
	rawGrants.SEOCode3[i] = str(rawGrants.SEOCode3[i])[0:2]
	rawGrants.SEOCode4[i] = str(rawGrants.SEOCode4[i])[0:2]
	rawGrants.SEOCode5[i] = str(rawGrants.SEOCode5[i])[0:2]


## Step 2: Generate Dummy Variables

RFCDCode1 = pd.get_dummies(rawGrants['RFCDCode1'])
RFCDCode1 = (rawGrants.RFCDPercentage1 * 
	RFCDCode1.transpose()/100).transpose()

RFCDCode2 = pd.get_dummies(rawGrants['RFCDCode2'])
RFCDCode2 = (rawGrants.RFCDPercentage2 * 
	RFCDCode2.transpose()/100).transpose()

RFCDCode3 = pd.get_dummies(rawGrants['RFCDCode3'])
RFCDCode3 = (rawGrants.RFCDPercentage3 * 
	RFCDCode3.transpose()/100).transpose()

RFCDCode4 = pd.get_dummies(rawGrants['RFCDCode4'])
RFCDCode4 = (rawGrants.RFCDPercentage4 * 
	RFCDCode4.transpose()/100).transpose()

RFCDCode5 = pd.get_dummies(rawGrants['RFCDCode5'])
RFCDCode5 = (rawGrants.RFCDPercentage5 * 
	RFCDCode5.transpose()/100).transpose()


SEOCode1 = pd.get_dummies(rawGrants['SEOCode1'])
SEOCode1 = (rawGrants.SEOPercentage1 * 
	SEOCode1.transpose()/100).transpose()

SEOCode2 = pd.get_dummies(rawGrants['SEOCode2'])
SEOCode2 = (rawGrants.SEOPercentage2 * 
	SEOCode2.transpose()/100).transpose()

SEOCode3 = pd.get_dummies(rawGrants['SEOCode3'])
SEOCode3 = (rawGrants.SEOPercentage3 * 
	SEOCode3.transpose()/100).transpose()

SEOCode4 = pd.get_dummies(rawGrants['SEOCode4'])
SEOCode4 = (rawGrants.SEOPercentage4 * 
	SEOCode4.transpose()/100).transpose()

SEOCode5 = pd.get_dummies(rawGrants['SEOCode5'])
SEOCode5 = (rawGrants.SEOPercentage5 * 
	SEOCode5.transpose()/100).transpose()


#2.1: Combine the seperate frames
result12 = RFCDCode1.append(RFCDCode2, ignore_index = False)
result23 = result12.append(RFCDCode3, ignore_index = False)
result34 = result23.append(RFCDCode4, ignore_index = False)
result45 = result34.append(RFCDCode5, ignore_index = False)

RFCDDummyFrame = result45.groupby(result45.index).sum()

newRFCDCol = list()
for l in range(len(RFCDDummyFrame.columns)):
	newRFCDCol.append('RFCD' + str(RFCDDummyFrame.columns[l]))

RFCDDummyFrame.columns = newRFCDCol

SEOResult12 = SEOCode1.append(SEOCode2, ignore_index = False)
SEOResult23 = SEOResult12.append(SEOCode3, ignore_index = False)
SEOResult34 = SEOResult23.append(SEOCode4, ignore_index = False)
SEOResult45 = SEOResult34.append(SEOCode5, ignore_index = False)

SEODummyFrame = SEOResult45.groupby(SEOResult45.index).sum()

newSEOCol = list()
for l in range(len(SEODummyFrame.columns)):
	newSEOCol.append('SEO' + str(SEODummyFrame.columns[l]))

SEODummyFrame.columns = newSEOCol


## Pull Everything together ##
grants = rawGrants.iloc[:,0:6]
grants = pd.concat([grants,SEODummyFrame],axis = 1)
grants = pd.concat([grants,RFCDDummyFrame],axis = 1)

#Check for NAs and categories in grants once again.
for m in grants.columns:
	print 'Column Name: ' + m
	print pd.Series(grants[m].values).unique()
	print ''
	print 'Number of Nulls (nan) for : ' + m
	print '# of Nulls: ' + str(grants[m].isnull().sum())

#Drop RFCD0.0 and SEO0.0.  These exist only when for example an RFCD or SEO was not used
# for example for the original RFCD2 column may not be used for an individual 
grants = grants.drop('RFCD0.0',1)
grants = grants.drop('SEO0.0',1)
rawGrants['Startdate'] = pd.to_datetime(pd.Series(rawGrants['Startdate']))

grants.to_csv('data/grants.csv')














