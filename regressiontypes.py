# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 06:06:32 2019
@author: Kevin Yang
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

from scipy import stats
stats.chisqprob = lambda chisq, df: stats.chi2.sf(chisq, df)
from sklearn.preprocessing import PolynomialFeatures

errorDialog = QtWidgets.QErrorMessage()
errorDialog.setWindowTitle('Error')

def linear_regression(self, y, x, isMultivariate):
    print('Performing Linear Regression!')
    QApplication.instance().processEvents()
    x1 = sm.add_constant(x)
    print (y)
    print (x)
    results = sm.OLS(y,x1).fit()
    
    if not isMultivariate:
        plot_linear_regression(self, x, y, results)
    else:
        clear_plot(self.regressionPlot)
    render_statistics(self, results)
        
def logistic_regression(self, y, x, isMultivariate):
    print('Performing Logistic Regression!')
    QApplication.instance().processEvents()
    x1 = sm.add_constant(x)
    results = sm.Logit(y, x1).fit()
    
    if not isMultivariate:
        plot_logistic_regression(self, x, y, results)
    else:
        clear_plot(self.regressionPlot)
    render_statistics(self, results)

def polynomial_regression(self, y, x, isMultivariate, degree):
    print('Performing Polynomial Regression!')
    QApplication.instance().processEvents()
    try:
        intDegree = int(degree)
    except:
        errorDialog.showMessage('Degree is not an integer')
    polynomialFeatures = PolynomialFeatures(degree=intDegree)
    xp = polynomialFeatures.fit_transform(x)
    results = sm.OLS(y,xp).fit()
    
    if not isMultivariate:
        plot_polynomial_regression(self, x, y, results, intDegree)
    else:
        clear_plot(self.regressionPlot)
    render_statistics(self, results)
    
def ridge_regression(self, y, x, isMultivariate):
    print('Performing Ridge Regression!')
    QApplication.instance().processEvents()
    x1 = sm.add_constant(x)
    results = sm.regression.linear_model.OLS(y,x1).fit_regularized(alpha=0)
    if not isMultivariate:
        errorDialog.showMessage('Ridge Regression should have more than one predictor')
    else:
        clear_plot(self.regressionPlot)
        render_statistics_for_regularized(self, results)
    
def lasso_regression(self, y, x, isMultivariate):
    print('Performing Lasso Regression!')
    QApplication.instance().processEvents()
    x1 = sm.add_constant(x)
    results = sm.regression.linear_model.OLS(y,x1).fit_regularized(alpha=1)
    
    if not isMultivariate:
        errorDialog.showMessage('Lasso Regression should have more than one predictor')
    else:
        clear_plot(self.regressionPlot)
        render_statistics_for_regularized(self, results)
    
def elasticNet_regression(self, y, x, isMultivariate, alpha):
    print('Performing ElasticNet Regression!')
    QApplication.instance().processEvents()
    try:
        intAlpha = float(alpha)
    except:
        errorDialog.showMessage('Alpha is not a number')
    x1 = sm.add_constant(x)
    results = sm.regression.linear_model.OLS(y,x1).fit_regularized(alpha=intAlpha)
    
    if not isMultivariate:
        errorDialog.showMessage('ElasticNet Regression should have more than one predictor')
    else:
        clear_plot(self.regressionPlot)
        render_statistics_for_regularized(self, results)
        
def render_statistics(self, results):
    print ('rendering statistics')
    QApplication.instance().processEvents()
    self.statisticsTextBox.setPlainText(results.summary().as_text()) 
    
def render_statistics_for_regularized(self, results):
    QApplication.instance().processEvents()
    parameters = results.params.to_frame()
    parameters.columns = ["coeff"]
    self.statisticsTextBox.setPlainText(parameters.to_string())
    
def clear_plot(regressionPlot):
    QApplication.instance().processEvents()
    regressionPlot.canvas.axes.clear()
    regressionPlot.canvas.draw()

from regressionplots import plot_linear_regression, plot_logistic_regression, plot_polynomial_regression