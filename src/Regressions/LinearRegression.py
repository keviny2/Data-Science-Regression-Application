from PyQt5.QtWidgets import QApplication
import statsmodels.api as sm

from .Regression import Regression

class LinearRegression(Regression):

    def __init__(self):
        super().__init__()
        self.regressionType = "Linear Regression"

    def doRegression(self, y, x):
        QApplication.instance().processEvents()
        x1 = sm.add_constant(x)
        results = sm.OLS(y, x1).fit()
        self.setParameters(y, x, results)

    def plot(self, regressionAppUI):
        QApplication.instance().processEvents()
        regressionLine = self.x * self.results.params[1] + self.results.params[0]
        self.renderPlot(self.x, self.y, regressionLine, regressionAppUI)
