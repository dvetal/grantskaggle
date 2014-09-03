# -*- coding: utf-8 -*-
"""
Grant Kaggle Competition:
Generate test/train, cv, and ml workflow

Created on Wed Sep  2 10:00:00 2014

@author: Don Vetal
"""

import csv
import pandas as pd
import numpy as np
import os
import datetime as dt
from sklearn import preprocessing

os.chdir('PublicProjects/Grants')

MLready = pd.read_csv('data/MLready.csv')
print MLready.shape
# 1 Split Test and train

# 1.1 convert MLready.Startdate to dates

MLready['Startdate'] = pd.to_datetime(pd.Series(MLready['Startdate']))
print MLready.shape

#Build Cross Validataion Function:
#This function is special because we are attempting to keep each of the folds bounded
#to a time range.


def createFolds(someDF,folds,holdoutDate):
	'''
	This function generates training folds and seperates a holdout for testing after
	a certain holdout Date (holdoutDate).

		Enter holdoutDate as a string in the format DD/MM/YY
		RETURNS: both a train (for CV) and a holdout test dataframe
	'''
	holdoutDate = dt.datetime.strptime(holdoutDate, "%d/%m/%y").date()
	print holdoutDate
	#Set aside start dates after holdoutDate as the final test.
	test = someDF[someDF.Startdate >= holdoutDate]
	print test.shape
	#Include everything before 2008 as the train.
	train = someDF[someDF.Startdate < holdoutDate]
	train = train.sort(['Startdate'])
	train['fold'] = np.linspace(1,folds+1,len(train)).astype(int)
	train.fold[train['fold'] > folds] = folds
	print train.shape
	return train, test

train, test = createFolds(MLready,folds=4,holdoutDate='01/01/08')

###############################################################################

features = [col for col in MLready.columns if col not in ['GrantStatus',
'GrantId','PersonID','folds','Startdate','Role','WithPHD']]

#Generate RF Fit
clf = RandomForestClassifier(n_jobs = -1)
RFfit = clf.fit(train[features],train['GrantStatus'])
#print 'Accuracy: ', clf.score(test[features],test['GrantStatus'])


#foldTrain = train[train['fold'] == 1]
#print 'Accuracy: ', clf.score(foldTrain[features],foldTrain['GrantStatus'])

performanceList = []
for m in range(1,folds+1):
	foldTrain = train[train['fold'] == m]
	Response = clf.predict(foldTrain[features]) == foldTrain['GrantStatus']
	foldTrain['Response'] = Response
	resultArray = foldTrain['Response'].groupby(foldTrain['GrantId']).sum().apply(float)/foldTrain.groupby(foldTrain['GrantId']).size().apply(float)
	performanceList.append(sum(resultArray)/len(resultArray))


###TEST RUN ####
performanceList = []
Response = clf.predict(test[features]) == test['GrantStatus']
test['Response'] = Response
resultArray = test['Response'].groupby(test['GrantId']).sum().apply(float)/test.groupby(test['GrantId']).size().apply(float)
performanceList.append(sum(resultArray)/len(resultArray))


def doRF(someDF):
	from sklearn.ensemble import RandomForestClassifier


def measurePerformance ():


























