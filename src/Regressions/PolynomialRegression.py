from PyQt5.QtWidgets import QApplication
import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures
import pandas as pd
import numpy as np
from .Regression import Regression
# from scipy import stats
# stats.chisqprob = lambda chisq, df: stats.chi2.sf(chisq, df)

class PolynomialRegression(Regression):

    def __init__(self, degree):
        super().__init__()
        self.degree = int(degree)
        self.regressionType = "Polynomial Regression"
        self.regressionLine = 0

    def doRegression(self, y, x):
        QApplication.instance().processEvents()
        try:
            intDegree = int(self.degree)
        except:
            raise(Exception('Degree is not an integer'))
        polynomialFeatures = PolynomialFeatures(degree=intDegree)
        xp = polynomialFeatures.fit_transform(x)
        results = sm.OLS(y, xp).fit()
        self.setParameters(y, x, results)

    def plot(self, regressionAppUI):
        QApplication.instance().processEvents()
        for i in range(1, self.degree + 1):
            self.regressionLine += np.power(self.x * self.results.params[i], i)
        sortedTable = self.sortTable()
        self.renderPlot(sortedTable[[self.x.columns[0]]], sortedTable[[self.y.columns[0]]],
                        sortedTable[['probability']], regressionAppUI)

    # Orders data in ascending order
    def sortTable(self):
        QApplication.instance().processEvents()
        tempTable = pd.concat((self.x, self.regressionLine, self.y), axis=1)
        tempTable.columns = [self.x.columns[0], 'probability', self.y.columns[0]]
        sortedTable = tempTable.sort_values(by=[self.x.columns[0]])
        return sortedTable
