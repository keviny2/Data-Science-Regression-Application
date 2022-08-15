from PyQt5.QtWidgets import QApplication
import statsmodels.api as sm
#from scipy import stats
from scipy.special import expit
#stats.chisqprob = lambda chisq, df: stats.chi2.sf(chisq, df)
import pandas as pd
from .Regression import Regression

class LogisticRegression(Regression):

    def __init__(self):
        super().__init__()
        self.regressionType = "Logistic Regression"
        self.regressionLine = None

    def doRegression(self, y, x):
        QApplication.instance().processEvents()
        x1 = sm.add_constant(x)
        results = sm.Logit(y, x1).fit()
        self.setParameters(y, x, results)

    def plot(self, regressionAppUI):
        QApplication.instance().processEvents()
        self.regressionLine = expit(self.x * self.results.params[1] + self.results.params[0])
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
