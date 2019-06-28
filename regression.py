# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 12:03:33 2019

@author: Kevin Yang
"""
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

from scipy import stats
stats.chisqprob = lambda chisq, df: stats.chi2.sf(chisq, df)
from sklearn import preprocessing

def perform_regression(self, regressionType, inputFilePath, standardize, multivariate, 
                       responseVariable, predictors, categoricalVariables):
    print ('performing regression')
    responseVariable, data = preprocess(inputFilePath, responseVariable, categoricalVariables,
                                        predictors, standardize)
    print ('finished preprocessing')
    fileName, fileExtension = os.path.splitext(inputFilePath)
    if (fileExtension == '.xlsx'):
        excel_regression(inputFilePath)
    elif (fileExtension == '.xlsm'):
        macro_excel_regression(inputFilePath)
    else:
        csv_regression(self, data, regressionType, responseVariable, multivariate)

def preprocess(inputFilePath, responseVariable, categoricalVariables,
               predictors, standardize):
    errorDialog = QtWidgets.QErrorMessage()
    _, categoricalVariablesList = get_variable_list(categoricalVariables)
    predictorVariablesString, predictorVariablesList = get_variable_list(predictors)
    responseVariableProcessed = responseVariable.strip()
    data = pd.read_csv(inputFilePath)
    if not os.path.exists(inputFilePath):
        errorDialog.showMessage('File path does not exist')
    if not responseVariableProcessed in data.columns:
        errorDialog.showMessage('Response Variable does not exist in data table')
    for categoricalVariable in categoricalVariablesList:
        if not categoricalVariable in data.columns:
            errorDialog.showMessage(f'{categoricalVariable} does not exist in data table')
    for predictor in predictorVariablesList:
        if not predictor in data.columns:
            errorDialog.showMessage(f'{predictor} does not exist in data table')
    
    print ('got through conditionals')        
    processedData = preprocess_data(data, categoricalVariablesList, predictorVariablesString,
                                    responseVariableProcessed, standardize)  
    return responseVariableProcessed, processedData

def preprocess_data(data, categoricalVariablesList, predictorVariablesString, 
                    responseVariableProcessed, standardize):
    dataDropNullColumns = data.dropna(how='any', axis=1)
    dataDropNullRows = dataDropNullColumns.dropna(how='any', axis=0)
    dataDropUnnammedColumns = dataDropNullRows.loc[:, ~dataDropNullRows.columns.str.contains('^Unnamed')]
    dataDropColumns = dataDropUnnammedColumns[[predictorVariablesString, responseVariableProcessed]]
    data = dataDropColumns.copy()
    
    for column in categoricalVariablesList:
        data[column] = data[column].astype('category')
        data[column] = data[column].cat.codes
        
    if (standardize == 2):
        predictors = data[[predictorVariablesString]]
        numCols = predictors.columns[predictors.dtypes.apply(lambda c: np.issubdtype(c, np.number))]
        scaler = preprocessing.StandardScaler()
        data[numCols] = scaler.fit_transform(data[numCols])
        
    return data
    
def get_variable_list(inputString):
    inputStringNoWhiteSpace = inputString.replace(" ", "")
    inputStringList = inputStringNoWhiteSpace.split(',')
    return inputStringNoWhiteSpace, inputStringList
        
def csv_regression(self, data, regressionType, responseVariable, multivariate):        
    print('CSV!')
    y = data[responseVariable]
    x1 = data.drop(responseVariable, 1)
    func = get_regression_func(regressionType)
    func(self, y, x1, multivariate)
    
def excel_regression(inputFilePath):
    print('Excel!')
    
def macro_excel_regression(inputFilePath):
    print('Macro!')
    
def get_regression_func(regressionType):
    regressionTypes = {
        1: "Linear Regression",
        "Logistic Regression": logistic_regression,
        3: "Polynomial Regression",
        4: "Stepwise Regression",
        5: "Ridge Regression",
        6: "Lasso Regression",
        7: "ElasticNet Regression"
        }
    func = regressionTypes.get(regressionType, lambda: "Invalid regression type")
    return func

from regressiontypes import logistic_regression