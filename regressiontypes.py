# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 06:06:32 2019

@author: Kevin Yang
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

from scipy import stats
stats.chisqprob = lambda chisq, df: stats.chi2.sf(chisq, df)

def logistic_regression(self, y, x1, multivariate):
    print('Performing Logistic Regression!')
    x = sm.add_constant(x1)
    results = sm.Logit(y, x).fit()
    return results
    
def linear_regression(self, y, x1, multivariate):
    print('Performing Linear Regression!')
    x = sm.add_constant(x1)
    results = sm.OLS(y,x).fit()
    return results
    
def render_plot(self, x, y, regressionType, multivariate):
    if (multivariate == 0):
        self.regressionPlot.canvas.axes.clear()
        self.regressionPlot.canvas.axes.scatter(x, y)
        self.regressionPlot.canvas.axes.set_title(regressionType)
        self.regressionPlot.canvas.draw()
    else:
        self.regressionPlot.canvas.axes.clear()
        self.regressionPlot.canvas.draw()
        
def render_statistics(self, results):
    self.statisticsTextBox.setPlainText(results.summary().as_text()) 