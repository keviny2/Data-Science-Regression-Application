from PyQt5.QtWidgets import QApplication

from src.Regressions.ElasticNetRegression import ElasticNetRegression
from src.Regressions.LassoRegression import LassoRegression
from src.Regressions.LinearRegression import LinearRegression
from src.Regressions.LogisticRegression import LogisticRegression
from src.Regressions.PolynomialRegression import PolynomialRegression
from src.Regressions.RidgeRegression import RidgeRegression


class RegressionFactory:

    def __init__(self, regressionType, regressionAppUI):
        self.regressionType = regressionType
        self.regressionAppUI = regressionAppUI

    # Determines what type of regression user selected and performs the regression
    # of interest
    def makeRegression(self):
        QApplication.instance().processEvents()
        func = self.getRegressionFunction(self.regressionType)
        return func()
        # y = preprocessedData[[responseVariable]]
        # x = preprocessedData.drop(responseVariable, 1)
        # func = get_regression_func(regressionType)
        # if func == elasticNet_regression:
        #     func(self, y, x, isMultivariate, alpha)
        # elif func == polynomial_regression:
        #     func(self, y, x, isMultivariate, degree)
        # else: 
        #     func(self, y, x, isMultivariate)
    
    # Returns function corresponding to regressionType parameter
    def getRegressionFunction(self, regressionType):
        regressionTypes = {
            "Linear Regression": self.makeLinearRegression,
            "Logistic Regression": self.makeLogisticRegression,
            "Polynomial Regression": self.makePolynomialRegression,
            "Ridge Regression": self.makeRidgeRegression,
            "Lasso Regression": self.makeLassoRegression,
            "ElasticNet Regression": self.makeElasticNetRegression
            }
        func = regressionTypes.get(regressionType, lambda: "Invalid regression type")
        return func

    def makeLinearRegression(self):
        return LinearRegression()

    def makeLogisticRegression(self):
        return LogisticRegression()

    def makePolynomialRegression(self):
        return PolynomialRegression(self.regressionAppUI.degreeTextBox.text())

    def makeRidgeRegression(self):
        return RidgeRegression()

    def makeLassoRegression(self):
        return LassoRegression()

    def makeElasticNetRegression(self):
        return ElasticNetRegression(self.regressionAppUI.alphaTextBox.text())