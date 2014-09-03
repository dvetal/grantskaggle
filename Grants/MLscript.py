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
from sklearn.ensemble import RandomForestClassifier

os.chdir('PublicProjects/Grants')

MLready = pd.read_csv('data/MLready.csv')
# 1 Split Test and train

# 1.1 convert MLready.Startdate to dates

MLready['Startdate'] = pd.to_datetime(pd.Series(MLready['Startdate']))

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

folds = 4

train, test = createFolds(MLready,folds=folds,holdoutDate='01/01/08')

###############################################################################

features = [col for col in MLready.columns if col not in ['GrantStatus',
'GrantId','PersonID','folds','Startdate','Role','WithPHD']]

#Generate RF Fit
clf = RandomForestClassifier(n_jobs = -1)
RFfit = clf.fit(train[features],train['GrantStatus'])

def randomForest(folds,train,test,features):
	performanceList = []
	RFfit = []
	for m in range(1,folds+1):
		#Generate this fold's test and train
		foldTrain = train[train['fold'] != m]
		foldTest = train[train['fold'] == m]
		#fit the train for this fold
		clf = RandomForestClassifier(n_jobs = -1)
		RFfit.append(clf.fit(foldTrain[features],foldTrain['GrantStatus']))
		#Test the fit against the fold's test
		Response = clf.predict(foldTest[features]) == foldTest['GrantStatus']
		foldTest['Response'] = Response
		#Out of the response groupby GrantId so we get one record for each grantID, and
		#sum the result and divide by the total number of records in a single GrantId
		resultArray = foldTest['Response'].groupby(foldTest['GrantId']).sum().apply(float)/foldTest.groupby(foldTest['GrantId']).size().apply(float)
		#append performance for this fold to a list
		performanceList.append(sum(resultArray)/len(resultArray))
		print 'In Sample Performance: for fold %d: %f' % (m, np.mean(performanceList))
	### TEST ###
	Response = clf.predict(test[features]) == test['GrantStatus']   
	test['Response'] = Response
	#Out of the response groupby GrantId so we get one record for each grantID, and
	#sum the result and divide by the total number of records in a single GrantId
	resultArray = test['Response'].groupby(test['GrantId']).sum().apply(float)/test.groupby(test['GrantId']).size().apply(float)
	#append performance for this fold to a list
	testResult = sum(resultArray)/len(resultArray)
	print 'Out of Sample Performance: ', testResult	
	return performanceList


###TEST RUN ####
#performanceList = []
#Response = clf.predict(test[features]) == test['GrantStatus']
#test['Response'] = Response
#resultArray = test['Response'].groupby(test['GrantId']).sum().apply(float)/test.groupby(test['GrantId']).size().apply(float)
#performanceList.append(sum(resultArray)/len(resultArray))
