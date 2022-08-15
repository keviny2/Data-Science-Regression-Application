import os
import pandas as pd
from PyQt5.QtWidgets import QApplication
import numpy as np
from sklearn import preprocessing

class Dataset:
    
    def __init__(self, inputFilePath, responseVariable, predictors, categoricalVariables):
        self.inputFilePath = inputFilePath
        self.categoricalVariablesList = self.__getVariableList(categoricalVariables)
        self.predictorVariablesList = self.__getVariableList(predictors)
        self.responseVariable = responseVariable.strip()
        self.dataset = self.readDataset()
        
    def readDataset(self):
        _, fileExtension = os.path.splitext(self.inputFilePath)

        if fileExtension == '.xlsx':
            return pd.read_excel(self.inputFilePath)
        elif fileExtension == '.csv':
            return pd.read_csv(self.inputFilePath)
        else:
            raise(Exception('Invalid file extension'))

    def validateVariableLists(self):
        missingColumnNames = ""
        if not self.responseVariable in self.dataset.columns:
            missingColumnNames += self.responseVariable + ','

        for predictor in self.predictorVariablesList:
            if not predictor in self.dataset.columns:
                missingColumnNames += predictor + ','

        for categoricalVariable in self.categoricalVariablesList:
            if not categoricalVariable in self.dataset.columns:
                missingColumnNames += categoricalVariable + ','

        if not missingColumnNames == "":
            missingColumnNames = missingColumnNames[:-1]
            raise(Exception(f'{missingColumnNames} not in the data table'))

    def preprocessDataset(self, standardize):
        QApplication.instance().processEvents()
        dataDropNullColumns = self.dataset.dropna(how='all', axis=1)
        dataDropNullRows = dataDropNullColumns.dropna(how='any', axis=0)
        dataDropUnnamedColumns = dataDropNullRows.loc[:, ~dataDropNullRows.columns.str.contains('^Unnamed')]
        relevantColumns = self.predictorVariablesList + [self.responseVariable]
        dataDropColumns = dataDropUnnamedColumns[relevantColumns]
        data = dataDropColumns.copy()
        
        if len(self.categoricalVariablesList) > 0:
            for column in self.categoricalVariablesList:
                data[column] = data[column].astype('category')
                data[column] = data[column].cat.codes
                
        if standardize == 2:
            predictors = data[self.predictorVariablesList]
            numericColumns = predictors.columns[predictors.dtypes.apply(lambda c: np.issubdtype(c, np.number))]
            scaler = preprocessing.StandardScaler()
            data[numericColumns] = scaler.fit_transform(data[numericColumns])
                
        self.dataset = data

    def __getVariableList(self, inputString):
        QApplication.instance().processEvents()
        if inputString:
            inputStringList = inputString.split(',')
            for idx, val in enumerate(inputStringList):
                inputStringList[idx] = inputStringList[idx].strip()
            return inputStringList
        else:
            return list()