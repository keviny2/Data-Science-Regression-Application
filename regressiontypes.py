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
    reg = sm.Logit(y, x)
    results = reg.fit()
    
    if multivariate == 0:
        self.regressionPlot.canvas.axes.clear()
        self.regressionPlot.canvas.axes.scatter(x1, y)
        self.regressionPlot.canvas.axes.set_title('Logistic Regression')
        self.regressionPlot.canvas.draw()
    else:
        self.regressionPlot.canvas.axes.clear()
        self.regressionPlot.canvas.axes.draw()
        
    self.statisticsTextBox.setPlainText(results.summary().as_csv())