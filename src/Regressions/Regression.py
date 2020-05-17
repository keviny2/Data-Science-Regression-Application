from PyQt5.QtWidgets import QApplication
import seaborn as sns
sns.set()

class Regression:

    def __init__(self):
        self.results = None
        self.isMultivariate = False
        self.y = None
        self.x = None
        self.regressionType = ""

    def doRegression(self, y, x):
        pass

    def plot(self, regressionAppUI):
        pass

    def setParameters(self, y, x, results):
        self.y = y
        self.x = x
        self.results = results
        self.isMultivariate = x.shape[1] > 1

    def renderPlot(self, x, y, regressionLine, regressionAppUI):
        QApplication.instance().processEvents()
        regressionAppUI.regressionPlot.canvas.axes.clear()
        regressionAppUI.regressionPlot.canvas.axes.set_title(self.regressionType)
        regressionAppUI.regressionPlot.canvas.axes.set_xlabel(str(x.columns[0]))
        regressionAppUI.regressionPlot.canvas.axes.set_ylabel(str(y.columns[0]))
        regressionAppUI.regressionPlot.canvas.axes.scatter(x, y)
        regressionAppUI.regressionPlot.canvas.axes.plot(x, regressionLine, lw=4, c='orange', label='regression line')
        regressionAppUI.regressionPlot.canvas.draw()
