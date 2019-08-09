# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 06:54:11 2019

@author: Kevin Yang
"""
from PyQt5.QtWidgets import QApplication
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

from scipy import stats
from scipy.special import expit
stats.chisqprob = lambda chisq, df: stats.chi2.sf(chisq, df)
from sklearn.preprocessing import PolynomialFeatures

def plot_linear_regression(self, x, y, results):
    print ('plotting linear regression')
    QApplication.instance().processEvents()
    regressionLine = x*results.params[1] + results.params[0]
    render_plot(self, x, y, regressionLine, "Linear Regression")
    
def plot_logistic_regression(self, x, y, results):
    print ('plotting logistic regression')
    QApplication.instance().processEvents()
    logisticRegressionLine = expit(x*results.params[1] + results.params[0])
    sortedTable = sort_table(x, y, logisticRegressionLine)
    render_plot(self, sortedTable[[x.columns[0]]], sortedTable[[y.columns[0]]], sortedTable[['probability']], "Logistic Regression")
    
def plot_polynomial_regression(self, x, y, results, degree):
    print ('plotting polynomial regression')
    QApplication.instance().processEvents()
    polynomialRegressionLine = 0
    for i in range(1, degree+1):
        polynomialRegressionLine += np.power(x*results.params[i], i)
    sortedTable = sort_table(x, y, polynomialRegressionLine)
    render_plot(self, sortedTable[[x.columns[0]]], sortedTable[[y.columns[0]]], sortedTable[['probability']], "Polynomial Regression")
    
def render_plot(self, x, y, regressionLine, regressionType):
    print('rendering plot')
    QApplication.instance().processEvents()
    self.regressionPlot.canvas.axes.clear()
    self.regressionPlot.canvas.axes.set_title(regressionType)
    self.regressionPlot.canvas.axes.set_xlabel(str(x.columns[0]))
    self.regressionPlot.canvas.axes.set_ylabel(str(y.columns[0]))
    self.regressionPlot.canvas.axes.scatter(x, y)
    self.regressionPlot.canvas.axes.plot(x, regressionLine, lw=4, c='orange', label='regression line')
    self.regressionPlot.canvas.draw()
    
def sort_table(x, y, regressionLine):
    QApplication.instance().processEvents()
    tempTable = pd.concat((x, regressionLine, y), axis=1)
    tempTable.columns = [x.columns[0], 'probability', y.columns[0]]
    sortedTable = tempTable.sort_values(by=[x.columns[0]])
    return sortedTable
    