from PyQt5.QtWidgets import QApplication
import statsmodels.api as sm
from .Regression import Regression

class RidgeRegression(Regression):

    def __init__(self):
        super().__init__()
        self.regressionType = "Ridge Regression"

    def doRegression(self, y, x):
        QApplication.instance().processEvents()
        x1 = sm.add_constant(x)
        results = sm.regression.linear_model.OLS(y, x1).fit_regularized(alpha=0)
        self.setParameters(y, x, results)

    def plot(self, regressionAppUI):
        QApplication.instance().processEvents()
        regressionLine = self.x * self.results.params[1] + self.results.params[0]
        self.renderPlot(self.x, self.y, regressionLine, regressionAppUI)
