# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 12:03:33 2019
@author: Kevin Yang
"""
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
import os
import numpy as np
import pandas as pd
import seaborn as sns
sns.set()

from scipy import stats
stats.chisqprob = lambda chisq, df: stats.chi2.sf(chisq, df)
from sklearn import preprocessing

## Error Dialog object that is displayed if process runs into any error
errorDialog = QtWidgets.QErrorMessage()
errorDialog.setWindowTitle('Error')

## Checks if file path is valid and determines what type of file has been
## selected for the regression then preprocesses data and runs regression
def perform_regression(self, regressionType, inputFilePath, standardize, 
                       degree, alpha, responseVariable, predictors, 
                       categoricalVariables):
    QApplication.instance().processEvents()
    if not os.path.exists(inputFilePath):
        errorDialog.showMessage('File path invalid')
        self.movie.stop()
        self.loaderLabel.hide()
        return
    
    _, fileExtension = os.path.splitext(inputFilePath)
        
    if (fileExtension == '.xlsx'):
        data = pd.read_excel(inputFilePath)
    elif (fileExtension == '.csv'):
        data = pd.read_csv(inputFilePath)
    else:
        return
    
    preprocessedData, preprocessedResponseVariable, isMultivariate = preprocess(self, data, responseVariable, categoricalVariables,
                                                                                 predictors, standardize, regressionType)
    
    do_regression(self, preprocessedData, regressionType, 
                  preprocessedResponseVariable, isMultivariate,
                  degree, alpha)
    
## Reads user inputs and checks to see if inputted response, predictor, and
## categorical variables exist in the selected file, then proceeds to 
## preprocess the data itself
def preprocess(self, data, responseVariable, categoricalVariables,
               predictors, standardize, regressionType):
    QApplication.instance().processEvents()
    categoricalVariablesList = get_variable_list(categoricalVariables)
    predictorVariablesList = get_variable_list(predictors)
    isMultivariate = len(predictorVariablesList) > 1
    preprocessedResponseVariable = responseVariable.strip()
    
    missingColumnNames = ""
    if not preprocessedResponseVariable in data.columns:
        missingColumnNames += preprocessedResponseVariable + ','
    for predictor in predictorVariablesList:
        if not predictor in data.columns:
            missingColumnNames += predictor + ','
    for categoricalVariable in categoricalVariablesList:
        if not categoricalVariable in data.columns:
            missingColumnNames += categoricalVariable + ','
    if not missingColumnNames == "":
        missingColumnNames = missingColumnNames[:-1]
        errorDialog.showMessage(f'{missingColumnNames} not in the data table')
        self.movie.stop()
        self.loaderLabel.hide()
        return
         
    preprocessedData = preprocess_data(data, categoricalVariablesList, predictorVariablesList,
                                    preprocessedResponseVariable, standardize)
    
    return preprocessedData, preprocessedResponseVariable, isMultivariate

## Preprocesses data by dropping any columns that are all null, removing rows 
## that contain null values, converting categorical data into its respective
## codes, and standardizing inputs if user checked the standardize checkbox
def preprocess_data(data, categoricalVariablesList, predictorVariablesList, 
                    preprocessedResponseVariable, standardize):
    QApplication.instance().processEvents()
    dataDropNullColumns = data.dropna(how='all', axis=1)
    dataDropNullRows = dataDropNullColumns.dropna(how='any', axis=0)
    dataDropUnnammedColumns = dataDropNullRows.loc[:, ~dataDropNullRows.columns.str.contains('^Unnamed')]
    relevantColumns = predictorVariablesList + [preprocessedResponseVariable]
    dataDropColumns = dataDropUnnammedColumns[relevantColumns]
    data = dataDropColumns.copy()
    
    if len(categoricalVariablesList) > 0:
        for column in categoricalVariablesList:
            data[column] = data[column].astype('category')
            data[column] = data[column].cat.codes
            
    if (standardize == 2):
        predictors = data[predictorVariablesList]
        numericColumns = predictors.columns[predictors.dtypes.apply(lambda c: np.issubdtype(c, np.number))]
        scaler = preprocessing.StandardScaler()
        data[numericColumns] = scaler.fit_transform(data[numericColumns])
            
    return data
    
## Returns an array of substrings from input string delimited by commas
def get_variable_list(inputString):
    QApplication.instance().processEvents()
    if inputString:
        inputStringNoWhiteSpace = inputString.replace(" ", "")
        inputStringList = inputStringNoWhiteSpace.split(',')
        return inputStringList
    else:
        return list()
        
## Determines what type of regression user selected and performs the regression
## of interest
def do_regression(self, preprocessedData, regressionType, responseVariable,
                  isMultivariate, degree, alpha):        
    QApplication.instance().processEvents()
    y = preprocessedData[[responseVariable]]
    x = preprocessedData.drop(responseVariable, 1)
    func = get_regression_func(regressionType)
    if func == elasticNet_regression:
        func(self, y, x, isMultivariate, alpha)
    elif func == polynomial_regression:
        func(self, y, x, isMultivariate, degree)
    else: 
        func(self, y, x, isMultivariate)
    
## Returns function corresponding to regressionType parameter
def get_regression_func(regressionType):
    regressionTypes = {
        "Linear Regression": linear_regression,
        "Logistic Regression": logistic_regression,
        "Polynomial Regression": polynomial_regression,
        "Ridge Regression": ridge_regression,
        "Lasso Regression": lasso_regression,
        "ElasticNet Regression": elasticNet_regression
        }
    func = regressionTypes.get(regressionType, lambda: "Invalid regression type")
    return func

from regressiontypes import logistic_regression, linear_regression, polynomial_regression, ridge_regression, lasso_regression, elasticNet_regression