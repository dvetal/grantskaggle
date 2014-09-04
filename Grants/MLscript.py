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

import matplotlib.pyplot as plt

os.chdir('PublicProjects/Grants')

#LOAD DATA
MLready = pd.read_csv('data/MLready.csv')
#Convert MLready.Startdate to dates
MLready['Startdate'] = pd.to_datetime(pd.Series(MLready['Startdate']))

###############
## FUNCTIONS ##
###############

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


def randomForest(folds,train,test,features):
	'''
	Performs random forest with cross validation based upon a list of features chosen
	from the data set.
	'''
	from sklearn.ensemble import RandomForestClassifier
	clf = RandomForestClassifier(n_jobs = -1)

	performanceList = []
	RFfit = []
	for m in range(1,folds+1):
		#Generate this fold's test and train
		foldTrain = train[train['fold'] != m]
		foldTest = train[train['fold'] == m]
		#fit the train for this fold	
		RFfit.append(clf.fit(foldTrain[features],foldTrain['GrantStatus']))
		#Test the fit against the fold's test
		Response = clf.predict(foldTest[features]) == foldTest['GrantStatus']
		foldTest['Response'] = Response
		#Out of the response groupby GrantId so we get one record for each grantID, and
		#sum the result and divide by the total number of records in a single GrantId
		resultArray = foldTest['Response'].groupby(foldTest['GrantId']).sum().apply(float)/foldTest.groupby(foldTest['GrantId']).size().apply(float)
		#append performance for this fold to a list
		performanceList.append(sum(resultArray)/len(resultArray))
	#	print 'In Sample Performance: for fold %d: %f' % (m, np.mean(performanceList))
	Bestfitfold = performanceList.index(max(performanceList)) + 1
	BestfitTrain = train[train['fold'] != Bestfitfold]
	Bestfit = clf.fit(BestfitTrain[features],BestfitTrain['GrantStatus'])
	testResponse = clf.predict(test[features]) == test['GrantStatus']
	test['Response'] = testResponse
	#Out of the response groupby GrantId so we get one record for each grantID, and
	#sum the result and divide by the total number of records in a single GrantId
	resultArray = test['Response'].groupby(test['GrantId']).sum().apply(float)/test.groupby(test['GrantId']).size().apply(float)
	#append performance for this fold to a list
	testResult = sum(resultArray)/len(resultArray)	
	return Bestfit, np.mean(performanceList), testResult


def knnRun(folds,train,test,features):
	'''
	Performs random forest with cross validation based upon a list of features chosen
	from the data set.
	'''
	from sklearn.neighbors import KNeighborsClassifier
	clf = KNeighborsClassifier(n_neighbors = 5)
	performanceList = []
	RFfit = []
	for m in range(1,folds+1):
		#Generate this fold's test and train
		foldTrain = train[train['fold'] != m]
		foldTest = train[train['fold'] == m]
		#fit the train for this fold	
		RFfit.append(clf.fit(foldTrain[features],foldTrain['GrantStatus']))
		#Test the fit against the fold's test
		Response = clf.predict(foldTest[features]) == foldTest['GrantStatus']
		foldTest['Response'] = Response
		#Out of the response groupby GrantId so we get one record for each grantID, and
		#sum the result and divide by the total number of records in a single GrantId
		resultArray = foldTest['Response'].groupby(foldTest['GrantId']).sum().apply(float)/foldTest.groupby(foldTest['GrantId']).size().apply(float)
		#append performance for this fold to a list
		performanceList.append(sum(resultArray)/len(resultArray))
	#	print 'In Sample Performance: for fold %d: %f' % (m, np.mean(performanceList))
	Bestfitfold = performanceList.index(max(performanceList)) + 1
	BestfitTrain = train[train['fold'] != Bestfitfold]
	Bestfit = clf.fit(BestfitTrain[features],BestfitTrain['GrantStatus'])
	testResponse = clf.predict(test[features]) == test['GrantStatus']
	test['Response'] = testResponse
	#Out of the response groupby GrantId so we get one record for each grantID, and
	#sum the result and divide by the total number of records in a single GrantId
	resultArray = test['Response'].groupby(test['GrantId']).sum().apply(float)/test.groupby(test['GrantId']).size().apply(float)
	#append performance for this fold to a list
	testResult = sum(resultArray)/len(resultArray)	
	return Bestfit, np.mean(performanceList), testResult


def bestFeatureList(top,fit,frame):
	'''
	Based upon a fit this function determines the column names for the most significant features.  This list can be used as
	an imput into another function to specify the features you want to fit and predict on.
	'''
	importanceValues = fit.feature_importances_
	indices = np.argsort(importanceValues)[::-1]
	return list(frame.columns[indices][:top])

##############
## WORKFLOW ##
##############

#Assign number of folds for crossvalidation
folds = 4

train, test = createFolds(MLready,folds=folds,holdoutDate='01/01/08')

#Assign features for machine learning to a list of column names
features = [col for col in MLready.columns if col not in ['GrantStatus',
'GrantId','PersonID','folds','Startdate','Role','WithPHD']]

numFeatures = []
trainResultList = []
testResultList = []

#Get an initial fit with many features
someFit, trainResult, testResult = knnRun(folds,train,test,features)

numFeatures.append(len(features))
trainResultList.append(trainResult)
testResultList.append(testResult)

featureSpaceSize = [1,5,10,15,20,50,100,150,200,300,350]
for n in featureSpaceSize:
	NewFeatures = bestFeatureList(top = n, fit = someFit, frame = train[features])
	someNewFit, trainResult, testResult = randomForest(folds = folds, train = train, test = test, features = NewFeatures)
	numFeatures.append(n)
	trainResultList.append(trainResult)
	testResultList.append(testResult)

#mess with hyperparameters

featurereductionTrain = plt.plot(numFeatures,trainResultList)
plt.show()

featurereductionTest = plt.plot(numFeatures,testResultList)
plt.show()


### THINGS TO DO ####

#Normalize data
#grid search over RF hyper parameters
#try other ML methods




















