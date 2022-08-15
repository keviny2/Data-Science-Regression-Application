from PyQt5.QtWidgets import QApplication

from Dataset import Dataset
from RegressionFactory import RegressionFactory
from Validator import Validator


class RegressionService:

    def __init__(self, regressionAppUI):
        self.regressionAppUI = regressionAppUI
        self.regressionType = regressionAppUI.typeComboBox.currentText()
        self.inputFilePath = regressionAppUI.inputFileTextBox.text()
        # standardize is 0 for unchecked and 2 for checked
        self.standardize = regressionAppUI.standardizeCheckBox.checkState()
        self.responseVariable = regressionAppUI.responseTextBox.text()
        self.predictors = regressionAppUI.predictorsTextBox.text()
        self.categoricalVariables = regressionAppUI.categoricalTextBox.text()
        self.regression = None
        self.isRegularized = self.regressionType in ['Ridge Regression', 'Lasso Regression', 'ElasticNet Regression']

    def performRegression(self):
        QApplication.instance().processEvents()
        preprocessedDataset = self.getDataset()
        regression = self.getRegression()
        self.doRegression(regression, preprocessedDataset)
        self.regression = regression

    def getDataset(self):
        QApplication.instance().processEvents()
        Validator.validateFilePath(self.inputFilePath)
        dataset = Dataset(self.inputFilePath, self.responseVariable, self.predictors, self.categoricalVariables)   
        dataset.validateVariableLists()
        dataset.preprocessDataset(self.standardize)
        return dataset

    def getRegression(self):
        QApplication.instance().processEvents()
        regressionFactory = RegressionFactory(self.regressionType, self.regressionAppUI)
        return regressionFactory.makeRegression()

    def doRegression(self, regression, preprocessedDataset):
        y = preprocessedDataset.dataset[[preprocessedDataset.responseVariable]]
        x = preprocessedDataset.dataset.drop(self.responseVariable, 1)
        regression.doRegression(y, x)

    def plotRegression(self):
        if not self.regression.isMultivariate:
            self.regression.plot(self.regressionAppUI)
        else:
            self.clearPlot()
        self.renderStatistics()

    def clearPlot(self):
        QApplication.instance().processEvents()
        self.regressionAppUI.regressionPlot.canvas.axes.clear()
        self.regressionAppUI.regressionPlot.canvas.draw()

    def renderStatistics(self):
        QApplication.instance().processEvents()
        if not self.isRegularized:
            self.regressionAppUI.statisticsTextBox.setPlainText(self.regression.results.summary().as_text())
        else:
            self.renderRegularizedStatistics()

    def renderRegularizedStatistics(self):
        QApplication.instance().processEvents()
        parameters = self.regression.results.params.to_frame()
        parameters.columns = ["coeff"]
        self.regressionAppUI.statisticsTextBox.setPlainText(parameters.to_string())
