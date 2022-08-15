import sys
import os
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

from RegressionService import RegressionService

errorDialog = QtWidgets.QErrorMessage()
errorDialog.setWindowTitle('Error')

class InteractiveRegressionApp:
    
    def __init__(self, regressionAppUI, regressionApp):
        self.regressionAppUI = regressionAppUI
        self.regressionApp = regressionApp

    def makeInteractive(self):
        # Code for interactive UI
        self.regressionAppUI.browseButton.clicked.connect(self.browse)
        self.regressionAppUI.browseButton.setAutoDefault(True)
        self.regressionAppUI.typeComboBox.currentTextChanged.connect(self.onComboBoxChanged)
        self.regressionAppUI.runRegressionButton.clicked.connect(self.runRegression)
        self.regressionAppUI.runRegressionButton.setAutoDefault(True)
        self.regressionAppUI.degreeLabel.hide()
        self.regressionAppUI.degreeTextBox.hide()
        self.regressionAppUI.alphaLabel.hide()
        self.regressionAppUI.alphaTextBox.hide()
        currDir = sys.path[0]
        loaderImgPath = os.path.join(currDir, '../images/ajax-loader.gif')
        self.regressionAppUI.movie = QtGui.QMovie(loaderImgPath)
        self.regressionAppUI.loaderLabel.setMovie(self.regressionAppUI.movie)
        windowIconImgPath = os.path.join(currDir, '../images/regression.png')
        self.regressionApp.setWindowIcon(QtGui.QIcon(windowIconImgPath))
        self.regressionApp.addToolBar(NavigationToolbar(self.regressionAppUI.regressionPlot.canvas, self.regressionAppUI.regressionPlot))
        # Code for menu bar
        self.regressionAppUI.actionClear_All.triggered.connect(self.clearAll)
        self.regressionAppUI.actionExit.triggered.connect(self.exitApp)
        self.regressionAppUI.actionSave_Graph.triggered.connect(self.saveGraph)
        self.regressionAppUI.actionSave_Statistics.triggered.connect(self.saveStatistics)

    # Executed when browse button is clicked
    def browse(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Browse", "", "CSV Files (*.csv);;Excel Files (*.xlsx)")
        self.regressionAppUI.inputFileTextBox.setText(fileName)
        
    # Show degree and alpha text box depending on what type of regression
    # user selects
    def onComboBoxChanged(self):
        if self.regressionAppUI.typeComboBox.currentText() == "Polynomial Regression":
            self.regressionAppUI.degreeLabel.show()
            self.regressionAppUI.degreeTextBox.show()
            self.regressionAppUI.alphaLabel.hide()
            self.regressionAppUI.alphaTextBox.hide()
        elif self.regressionAppUI.typeComboBox.currentText() == "ElasticNet Regression":
            self.regressionAppUI.degreeLabel.hide()
            self.regressionAppUI.degreeTextBox.hide()
            self.regressionAppUI.alphaLabel.show()
            self.regressionAppUI.alphaTextBox.show()
        else:
            self.regressionAppUI.degreeLabel.hide()
            self.regressionAppUI.degreeTextBox.hide()
            self.regressionAppUI.alphaLabel.hide()
            self.regressionAppUI.alphaTextBox.hide()
       
    # Restores form to initial state
    def clearAll(self):
        index = self.regressionAppUI.typeComboBox.findText("")
        self.regressionAppUI.typeComboBox.setCurrentIndex(index)
        self.regressionAppUI.inputFileTextBox.setText("")
        self.regressionAppUI.standardizeCheckBox.setChecked(False)
        self.regressionAppUI.degreeTextBox.setText("")
        self.regressionAppUI.alphaTextBox.setText("")
        self.regressionAppUI.responseTextBox.setText("")
        self.regressionAppUI.predictorsTextBox.setText("")
        self.regressionAppUI.categoricalTextBox.setText("")
        self.regressionAppUI.statisticsTextBox.setPlainText("")
        self.regressionAppUI.regressionPlot.canvas.axes.clear()
        self.regressionAppUI.regressionPlot.canvas.draw()
        
    # Closes application
    def exitApp(self):
        sys.exit()
        
    # Opens file explorer for user to save graph as a png file
    def saveGraph(self):
        filePath, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save Image", "", "PNG File (*.png);;PDF File (*.pdf)")
        self.regressionAppUI.regressionPlot.canvas.figure.savefig(filePath)
        
    # Opens file explorer for user to save statistics as a txt file
    def saveStatistics(self):
        filePath, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save File", "", "Text File (*.txt);;CSV File (*.csv);;JSON File (*.json)")
        with open(filePath, 'a+') as f:
            f.write(self.regressionAppUI.statisticsTextBox.toPlainText())
        
    # Executed when user clicks runRegression button
    def runRegression(self):
        self.regressionAppUI.loaderLabel.show()
        self.regressionAppUI.movie.start()
        QApplication.instance().processEvents()

        try: 
            regressionService = RegressionService(self.regressionAppUI)
            regressionService.performRegression()
            regressionService.plotRegression()

            QApplication.instance().processEvents()
            self.regressionAppUI.movie.stop()
            self.regressionAppUI.loaderLabel.hide()
        except Exception as error:
            errorDialog.showMessage(error.args[0])
            self.regressionAppUI.movie.stop()
            self.regressionAppUI.loaderLabel.hide()
