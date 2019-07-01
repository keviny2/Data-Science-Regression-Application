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
    
    fileName, fileExtension = os.path.splitext(inputFilePath)
    if not os.path.exists(inputFilePath):
        errorDialog = QtWidgets.QErrorMessage()
        errorDialog.showMessage('File path does not exist')
        
    if (fileExtension == '.xlsx'):
        data = pd.read_excel(inputFilePath)
    elif (fileExtension == '.csv'):
        data = pd.read_csv(inputFilePath)
    else:
        return
    
    preprocessedResponseVariable, preprocessedData = preprocess(data, responseVariable, categoricalVariables,
                                                                predictors, standardize)
    
    do_regression(self, data, preprocessedData, regressionType, preprocessedResponseVariable, multivariate)
    
def preprocess(data, responseVariable, categoricalVariables,
               predictors, standardize):
    errorDialog = QtWidgets.QErrorMessage()
    _, categoricalVariablesList = get_variable_list(categoricalVariables)
    predictorVariablesString, predictorVariablesList = get_variable_list(predictors)
    preprocessedResponseVariable = responseVariable.strip()
    
    if not preprocessedResponseVariable in data.columns:
        errorDialog.showMessage('Response Variable does not exist in data table')
    for categoricalVariable in categoricalVariablesList:
        if not categoricalVariable in data.columns:
            errorDialog.showMessage(f'{categoricalVariable} does not exist in data table')
    for predictor in predictorVariablesList:
        if not predictor in data.columns:
            errorDialog.showMessage(f'{predictor} does not exist in data table')
         
    preprocessedData = preprocess_data(data, categoricalVariablesList, predictorVariablesString,
                                    preprocessedResponseVariable, standardize)  
    return preprocessedResponseVariable, preprocessedData

def preprocess_data(data, categoricalVariablesList, predictorVariablesString, 
                    preprocessedResponseVariable, standardize):
    dataDropNullColumns = data.dropna(how='any', axis=1)
    dataDropNullRows = dataDropNullColumns.dropna(how='any', axis=0)
    dataDropUnnammedColumns = dataDropNullRows.loc[:, ~dataDropNullRows.columns.str.contains('^Unnamed')]
    dataDropColumns = dataDropUnnammedColumns[[predictorVariablesString, preprocessedResponseVariable]]
    data = dataDropColumns.copy()
    
    if categoricalVariablesList[0]:
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
        
def do_regression(self, data, preprocessedData, regressionType, responseVariable, multivariate):        
    print('doing regression!')
    y = preprocessedData[responseVariable]
    x1 = preprocessedData.drop(responseVariable, 1)
    func = get_regression_func(regressionType)
    results = func(self, y, x1, multivariate)

    render_plot(self, x, y, regressionType, multivariate, results.params)
    render_statistics(self, results)
    
def get_regression_func(regressionType):
    regressionTypes = {
        "Linear Regression": linear_regression,
        "Logistic Regression": logistic_regression,
        3: "Polynomial Regression",
        4: "Stepwise Regression",
        5: "Ridge Regression",
        6: "Lasso Regression",
        7: "ElasticNet Regression"
        }
    func = regressionTypes.get(regressionType, lambda: "Invalid regression type")
    return func

def render_plot(self, x, y, regressionType, multivariate, params):
    if (multivariate == 0):
        self.regressionPlot.canvas.axes.clear()
        self.regressionPlot.canvas.axes.scatter(x, y)
        yhat = x*params.size + params.const
        print (x)
        print (yhat, params)
        fig = self.regressionPlot.canvas.axes.plot(x, yhat, lw=4, c='orange', label='regression line')
        self.regressionPlot.canvas.axes.set_title(regressionType)
        self.regressionPlot.canvas.draw()
    else:
        self.regressionPlot.canvas.axes.clear()
        self.regressionPlot.canvas.draw()
        
def render_statistics(self, results):
    self.statisticsTextBox.setPlainText(results.summary().as_text()) 

from regressiontypes import logistic_regression, linear_regression