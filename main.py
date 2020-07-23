# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import os
import pandas as pd
from threading import Thread
import RDG.generator as gen
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import pathlib
dir_path = pathlib.Path(__file__).parent.absolute()
import CUDA.matcher as matcher
import gui_functions as gf

import numpy
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=500, height=400, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class Ui_MainWindow(object):
    path_column_num_dic = dict()
    current_md_dataset = ""
    current_page = 0
    matcher = None

    def algorithmSpeedComparison(self):
        data_path = self.datasetComboBox.currentText()
        if os.path.exists(data_path):
            domains = pd.read_csv(data_path, encoding = "ISO-8859-1", sep = ',', dtype='unicode', header = None)
            domain_list = self.createDomainList(domains, data_path)
            print(domain_list)
            if  isinstance(domain_list, bool):
                return

            algs = ['Levenshtein', 'Hamming', 'KMP', 'Rabin-Karp', 'Naive']
            self.sc.setParent(None)
            self.sc = MplCanvas(self, width=5, height=900, dpi=70)
            for alg in algs:
                if self.matcher is not None:
                    domains, times = self.matcher.is_malicious(domain_list, 'GPU', alg)
                    self.sc.axes.plot([(i+1) for i in range(len(times))], times, label=alg, linestyle='-.')
                    
                else:
                    self.displayError('You need to load the gpu with data')
            self.sc.axes.set_xlabel('Number of Domains')
            self.sc.axes.set_ylabel('Time (seconds)')
            self.sc.axes.set_title(f'Comparison of Algorithms on GPU (Time vs Number of domains')
            self.sc.axes.legend()

            self.sc.axes.grid(True)
            self.verticalLayout.addWidget(self.sc)
        else:
            self.displayError('Please select a valid dataset')
    def setupMatcher(self):
        db = gf.check_db_connection()
        gf.create_local_data(db)
        path = str(self.maliciousDatasetComboBox.currentText())
        #data_path = str(dir_path) + '\\localdata.csv'
        if os.path.exists(path):
            self.matcher = matcher.Matcher(path)
            self.matcher.load_gpu()
    def getDomainColumn(self, widget):
        i, okPressed = QtWidgets.QInputDialog.getInt(widget, "Enter the domain column","Column #:", 0, 0, 200, 1)
        if okPressed:
            return i
        return False

    def generateRandomDataClicked(self):
        rdg = gen.Generator()
        rdg.generate(100000)

    def maliciousDatasetComboBoxChanged(self, value):
        self.dataLoadCounter = 0
        while self.domainTable.rowCount() > 0:
            self.domainTable.removeRow(0)
        self.current_md_dataset = value
        self.updateTableView(value)
    def insertDataToDomainTable(self, data, path):
        high = self.dataLoadCounter + 1000
        print(len(data))
        print(self.dataLoadCounter)
        print(min(self.dataLoadCounter, len(data)))
        upper = min(high, len(data))

        for i in range(self.dataLoadCounter, upper, 1):
            #print('what')
            self.domainTable.insertRow(i-self.dataLoadCounter)
            print(data[self.path_column_num_dic[path]][i])
            self.domainTable.setItem(i-self.dataLoadCounter, 0, QtWidgets.QTableWidgetItem(str(data[self.path_column_num_dic[path]][i])))


    def updateTableView(self, dataFilePath):
        if os.path.exists(dataFilePath):
            data = pd.read_csv(dataFilePath, encoding = "ISO-8859-1", sep = ',', dtype='unicode', header = None)
            #self.getDomainColumn(self.centralwidget)
            thread = Thread(target = self.insertDataToDomainTable, args = (data, dataFilePath))
            thread.start()
            
            
    def addNewDatasetClick(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, "Choose Data", "", "csv(*.csv)")
        if '.csv' in file[1]:
            if os.path.exists(file[0]):
                col = self.getDomainColumn(self.centralwidget)
                while not isinstance(col, int):
                    col = self.getDomainColumn(self.centralwidget)
                self.path_column_num_dic[file[0]] = col
                self.maliciousDatasetComboBox.addItem(file[0])
                self.pageNumberLineEdit.setText('0')
            #self.getInteger()
                #self.updateTableView(file[0])
        print(file)
    
    def nextPageClicked(self):
        while self.domainTable.rowCount() > 0:
            self.domainTable.removeRow(0)
        self.pageNumberLineEdit.setText(str(self.current_page + 1))
        self.current_page = self.current_page + 1
        self.dataLoadCounter = self.dataLoadCounter + 1000
        self.updateTableView(self.current_md_dataset)
    def previousPageClicked(self):
        
        if self.dataLoadCounter >= 1000:
            while self.domainTable.rowCount() > 0:
                self.domainTable.removeRow(0)
            self.dataLoadCounter = self.dataLoadCounter - 1000
            self.updateTableView(self.current_md_dataset)
            self.pageNumberLineEdit.setText(str(self.current_page - 1))
            self.current_page = self.current_page - 1
    def goToPageClicked(self):
        try:
            val = self.pageNumberLineEdit.text()
            val = int(val)
            self.current_page = val - 1
            self.dataLoadCounter = (val - 1) * 1000
            self.nextPageClicked()
        except ValueError:
           self.displayError('Error parsing page number')
    def displayError(self, text):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(text)
        msg.setWindowTitle("Error")
        msg.exec_()
    def addDatasetClick(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, "Choose Data", "", "csv(*.csv)")
        if '.csv' in file[1]:
            if os.path.exists(file[0]):
                col = self.getDomainColumn(self.centralwidget)
                while not isinstance(col, int):
                    col = self.getDomainColumn(self.centralwidget)
                self.path_column_num_dic[file[0]] = col
                self.datasetComboBox.addItem(file[0])
    def createDomainList(self, domains, data_path):
        domain_list_pd = domains[self.path_column_num_dic[data_path]]
        print('oof')
        print(domain_list_pd)
        domain_list = []
        import random as rng

        samples = 0
        try:
            samples = int(self.sampleSizeTextBox.text())
        except ValueError:
            self.displayError('Enter a valid number of samples.')
            return False

        if self.duplicatesCheckbox.isChecked():
            for i in range(samples):
                domain_list.append(domain_list_pd[rng.randrange(len(domain_list_pd))])
        else:
            return domain_list_pd
        return domain_list
    def startProcessClicked(self):
        data_path = self.datasetComboBox.currentText()
        if os.path.exists(data_path):
            domains = pd.read_csv(data_path, encoding = "ISO-8859-1", sep = ',', dtype='unicode', header = None)
            domain_list = self.createDomainList(domains, data_path)
            print(domain_list)
            if  isinstance(domain_list, bool):
                return
            if self.matcher is not None:
                currentAlgorithm = self.algorithmComboBox.currentText()
                alg = ''
                if 'Levenshtein' in currentAlgorithm:
                    alg = 'Levenshtein'
                elif 'Hamming' in currentAlgorithm:
                    alg = 'Hamming'
                elif 'KMP' in currentAlgorithm:
                    alg = 'KMP'
                elif 'Rabin-Karp' in currentAlgorithm:
                    alg = 'Rabin-Karp'
                else:
                    alg = 'Naive'
                domains, times = self.matcher.is_malicious(domain_list, 'GPU', alg)
                self.sc.setParent(None)
                self.sc = MplCanvas(self, width=5, height=900, dpi=70)
                
                self.sc.axes.plot([(i+1) for i in range(len(times))], times, label='GPU', linestyle='-.')
                self.sc.axes.set_xlabel('Number of Domains')
                self.sc.axes.set_ylabel('Time (seconds)')
                self.sc.axes.set_title(f'Time vs Number of Domains using {alg} algorithm on GPU')
                self.sc.axes.legend()

                self.sc.axes.grid(True)
                self.verticalLayout.addWidget(self.sc)
            else:
                self.displayError('You need to load the gpu with data')
        else:
            self.displayError('Please select a valid dataset')
    def executeCPU(self):
        data_path = self.datasetComboBox.currentText()
        if os.path.exists(data_path):
            domains = pd.read_csv(data_path, encoding = "ISO-8859-1", sep = ',', dtype='unicode', header = None)
            domain_list = self.createDomainList(domains, data_path)
            if  isinstance(domain_list, bool):
                return
            if self.matcher is not None:
                currentAlgorithm = self.algorithmComboBox.currentText()
                alg = ''
                if 'Levenshtein' in currentAlgorithm:
                    alg = 'Levenshtein'
                elif 'Hamming' in currentAlgorithm:
                    alg = 'Hamming'
                else:
                    alg = 'Naive'
                domains, times = self.matcher.is_malicious(domain_list, 'CPU', alg)
                self.sc.axes.plot([(i+1) for i in range(len(times))], times, label='CPU', linestyle='-.')
                self.sc.axes.set_xlabel('Number of Domains')
                self.sc.axes.set_ylabel('Time (seconds)')
                self.sc.axes.set_title(f'Time vs Number of Domains using {alg} algorithm on GPU and CPU')
                self.sc.axes.legend()
                
                self.sc.axes.grid(True)
                self.verticalLayout.addWidget(self.sc)
            else:
                self.displayError('You need to load the gpu with data')
        else:
            self.displayError('Please select a valid dataset')
    def speedTest(self):
        self.startProcessClicked()
        self.executeCPU()

    def setupButtons(self):
        self.addNewDatasetButton.clicked.connect(self.addNewDatasetClick)
        self.maliciousDatasetComboBox.currentTextChanged.connect(self.maliciousDatasetComboBoxChanged)
        self.generateRandomDatasetButton.clicked.connect(self.generateRandomDataClicked)
        self.nextPageButton.clicked.connect(self.nextPageClicked)
        self.previousPageButton.clicked.connect(self.previousPageClicked)
        self.goToPageButton.clicked.connect(self.goToPageClicked)
        self.loadDataButton.clicked.connect(self.setupMatcher)
        self.startButton.clicked.connect(self.startProcessClicked)
        self.addDatasetButton.clicked.connect(self.addDatasetClick)
        self.speedTestButton.clicked.connect(self.speedTest)
        self.algorithmSpeedTestButton.clicked.connect(self.algorithmSpeedComparison)
    def setupUi(self, MainWindow):
        self.dataLoadCounter = 0
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1103, 918)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(18, 18, 18))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(183, 39, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(18, 18, 18))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(24, 120, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(18, 18, 18))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(18, 18, 18))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(151, 247, 211))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(18, 18, 18))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(183, 39, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(18, 18, 18))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(24, 120, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(18, 18, 18))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(18, 18, 18))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(151, 247, 211))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(24, 120, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(18, 18, 18))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(183, 39, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(18, 18, 18))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(24, 120, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(18, 18, 18))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(24, 120, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(24, 120, 83))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(18, 18, 18))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(18, 18, 18))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(48, 240, 167))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        MainWindow.setPalette(palette)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(49, 49, 49))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 229, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(226, 186, 227))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 72, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(132, 96, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(49, 49, 49))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(49, 49, 49))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(226, 199, 227))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(49, 49, 49))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 229, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(226, 186, 227))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 72, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(132, 96, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(49, 49, 49))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(49, 49, 49))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(226, 199, 227))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 72, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(49, 49, 49))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 229, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(226, 186, 227))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 72, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(132, 96, 133))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 72, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(99, 72, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(49, 49, 49))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(49, 49, 49))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(198, 144, 200))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.centralwidget.setPalette(palette)
        self.centralwidget.setStyleSheet("QWidget {\n"
"    background-color:#313131;\n"
"}\n"
"QPushButton{\n"
"    background-color: #e43f5a;\n"
"border: none;\n"
"  color: white;\n"
"  padding:10px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 12px;\n"
"  margin: 4px 2px;\n"
"border-radius: 12px;\n"
"}\n"
"QGroupBox {\n"
"    color: white;\n"
"    border: none;\n"
"background-color: #414141;\n"
"}\n"
"\n"
"QTabWidget::tab {\n"
"    background-color: red;\n"
"}\n"
"\n"
"QTableWidget {\n"
"color: red;\n"
"    background-color: red;\n"
"}\n"
"\n"
"QTabWidget::pane { border: 0; } QLabel { color:white;} \n QSpinBox {color:white;}")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setAcceptDrops(False)
        self.tabWidget.setStyleSheet("background-color: #414141;\n"
"border: none; \n"
"QTabWidget::pane \n"
"{\n"
"     border: 0;\n"
" }\n"
"QPushButton{\n"
"    background-color: #e43f5a;\n"
"border: none;\n"
"  color: white;\n"
"  padding:10px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 12px;\n"
"  margin: 4px 2px;\n"
"border-radius: 12px;\n"
"}")
        self.tabWidget.setObjectName("tabWidget")
        self.dataTab = QtWidgets.QWidget()
        self.dataTab.setStyleSheet("border: 0;\n"
"QPushButton{\n"
"    background-color: #e43f5a;\n"
"border: none;\n"
"  color: white;\n"
"  padding:10px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 12px;\n"
"  margin: 4px 2px;\n"
"border-radius: 12px;\n"
"} \n")
        self.dataTab.setObjectName("dataTab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.dataTab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.dataTabMainLayout = QtWidgets.QHBoxLayout()
        self.dataTabMainLayout.setObjectName("dataTabMainLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_2 = QtWidgets.QLabel(self.dataTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: #e43f5a;")
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.maliciousDatasetComboBox = QtWidgets.QComboBox(self.dataTab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.maliciousDatasetComboBox.setFont(font)
        self.maliciousDatasetComboBox.setStyleSheet("background-color: #e43f5a;")
        self.maliciousDatasetComboBox.setObjectName("maliciousDatasetComboBox")
        self.gridLayout_3.addWidget(self.maliciousDatasetComboBox, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.dataTab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #e43f5a;\n"
"font-size: 12;")
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 3, 0, 1, 1)
        self.searchBar = QtWidgets.QLineEdit(self.dataTab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.searchBar.setFont(font)
        self.searchBar.setStatusTip("")
        self.searchBar.setStyleSheet("background-color: #e43f5a;\n"
"color: white;")
        self.searchBar.setObjectName("searchBar")
        self.gridLayout_3.addWidget(self.searchBar, 4, 0, 1, 1)
        self.domainTable = QtWidgets.QTableWidget(self.dataTab)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.domainTable.setFont(font)
        self.domainTable.setStatusTip("")
        self.domainTable.setStyleSheet("background-color: #525252; color: #e43f5a; font-weight: bold;")
        self.domainTable.setShowGrid(True)
        self.domainTable.setCornerButtonEnabled(False)
        self.domainTable.setObjectName("domainTable")
        self.domainTable.setColumnCount(1)

        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setHorizontalHeaderItem(0, item)

        self.domainTable.horizontalHeader().setCascadingSectionResizes(True)
        self.domainTable.horizontalHeader().setDefaultSectionSize(400)
        self.domainTable.horizontalHeader().setMinimumSectionSize(400)
        self.domainTable.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_3.addWidget(self.domainTable, 5, 0, 1, 1)
        self.dataTabMainLayout.addLayout(self.gridLayout_3)
        self.dataTabMainLayoutV1 = QtWidgets.QVBoxLayout()
        self.dataTabMainLayoutV1.setObjectName("dataTabMainLayoutV1")
        spacerItem1 = QtWidgets.QSpacerItem(20, 120, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.dataTabMainLayoutV1.addItem(spacerItem1)
        self.addNewDatasetButton = QtWidgets.QPushButton(self.dataTab)
        self.addNewDatasetButton.setStyleSheet("QPushButton{\n"
"    background-color: #e43f5a;\n"
"border: none;\n"
"  color: white;\n"
"  padding:10px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 12px;\n"
"  margin: 4px 2px;\n"
"border-radius: 12px;\n"
"transition-duration: 0.8s;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #525252;\n"
"    color: white;\n"
"}\n"
"\n"
"")
        self.addNewDatasetButton.setObjectName("addNewDatasetButton")
        self.dataTabMainLayoutV1.addWidget(self.addNewDatasetButton)
        self.loadDataButton = QtWidgets.QPushButton(self.dataTab)
        self.loadDataButton.setStyleSheet("QPushButton{\n"
"    background-color: #e43f5a;\n"
"border: none;\n"
"  color: white;\n"
"  padding:10px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 12px;\n"
"  margin: 4px 2px;\n"
"border-radius: 12px;\n"
"transition-duration: 0.8s;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #525252;\n"
"    color: white;\n"
"}\n"
"\n"
"")
        self.loadDataButton.setObjectName("loadDataButton")
        self.dataTabMainLayoutV1.addWidget(self.loadDataButton)
        self.generateRandomDatasetButton = QtWidgets.QPushButton(self.dataTab)
        self.generateRandomDatasetButton.setStyleSheet("QPushButton{\n"
"    background-color: #e43f5a;\n"
"border: none;\n"
"  color: white;\n"
"  padding:10px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 12px;\n"
"  margin: 4px 2px;\n"
"border-radius: 12px;\n"
"transition-duration: 0.8s;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #525252;\n"
"    color: white;\n"
"}\n"
"\n"
"")
        self.generateRandomDatasetButton.setObjectName("generateRandomDatasetButton")
        self.dataTabMainLayoutV1.addWidget(self.generateRandomDatasetButton)
        self.AppendDataButton = QtWidgets.QPushButton(self.dataTab)
        self.AppendDataButton.setStyleSheet("QPushButton{\n"
"    background-color: #e43f5a;\n"
"border: none;\n"
"  color: white;\n"
"  padding:10px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 12px;\n"
"  margin: 4px 2px;\n"
"border-radius: 12px;\n"
"transition-duration: 0.8s;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #525252;\n"
"    color: white;\n"
"}\n"
"\n"
"")
        self.AppendDataButton.setObjectName("AppendDataButton")
        self.dataTabMainLayoutV1.addWidget(self.AppendDataButton)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.dataTabMainLayoutV1.addItem(spacerItem2)
        self.nextPageButton = QtWidgets.QPushButton(self.dataTab)
        self.nextPageButton.setStyleSheet("QPushButton{\n"
"    background-color: #e43f5a;\n"
"border: none;\n"
"  color: white;\n"
"  padding:10px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 12px;\n"
"  margin: 4px 2px;\n"
"border-radius: 12px;\n"
"transition-duration: 0.8s;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #525252;\n"
"    color: white;\n"
"}\n"
"\n"
"")
        self.nextPageButton.setObjectName("nextPageButton")
        self.dataTabMainLayoutV1.addWidget(self.nextPageButton)
        self.previousPageButton = QtWidgets.QPushButton(self.dataTab)
        self.previousPageButton.setStyleSheet("QPushButton{\n"
"    background-color: #e43f5a;\n"
"border: none;\n"
"  color: white;\n"
"  padding:10px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 12px;\n"
"  margin: 4px 2px;\n"
"border-radius: 12px;\n"
"transition-duration: 0.8s;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #525252;\n"
"    color: white;\n"
"}\n"
"\n"
"")
        self.previousPageButton.setObjectName("previousPageButton")
        self.dataTabMainLayoutV1.addWidget(self.previousPageButton)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.label_7 = QtWidgets.QLabel(self.dataTab)
        self.label_7.setStyleSheet("color: white;")
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_2.addWidget(self.label_7)
        self.pageNumberLineEdit = QtWidgets.QLineEdit(self.dataTab)
        self.pageNumberLineEdit.setText('0')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pageNumberLineEdit.sizePolicy().hasHeightForWidth())
        self.pageNumberLineEdit.setSizePolicy(sizePolicy)
        self.pageNumberLineEdit.setStyleSheet("background-color: #e43f5a;\n"
"color: white;\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"")
        self.pageNumberLineEdit.setObjectName("pageNumberLineEdit")
        self.horizontalLayout_2.addWidget(self.pageNumberLineEdit)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.dataTabMainLayoutV1.addLayout(self.horizontalLayout_2)
        self.goToPageButton = QtWidgets.QPushButton(self.dataTab)
        self.goToPageButton.setStyleSheet("QPushButton{\n"
"    background-color: #e43f5a;\n"
"border: none;\n"
"  color: white;\n"
"  padding:10px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 12px;\n"
"  margin: 4px 2px;\n"
"border-radius: 12px;\n"
"transition-duration: 0.8s;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #525252;\n"
"    color: white;\n"
"}\n"
"\n"
"")
        self.goToPageButton.setObjectName("goToPageButton")
        self.dataTabMainLayoutV1.addWidget(self.goToPageButton)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.dataTabMainLayoutV1.addItem(spacerItem5)
        self.addButton = QtWidgets.QPushButton(self.dataTab)
        self.addButton.setStyleSheet("QPushButton{\n"
"    background-color: #e43f5a;\n"
"border: none;\n"
"  color: white;\n"
"  padding:10px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 12px;\n"
"  margin: 4px 2px;\n"
"border-radius: 12px;\n"
"transition-duration: 0.8s;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #525252;\n"
"    color: white;\n"
"}\n"
"\n"
"")
        self.addButton.setObjectName("addButton")
        self.dataTabMainLayoutV1.addWidget(self.addButton)
        self.deleteEntryButton = QtWidgets.QPushButton(self.dataTab)
        self.deleteEntryButton.setStyleSheet("QPushButton{\n"
"    background-color: #e43f5a;\n"
"border: none;\n"
"  color: white;\n"
"  padding:10px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 12px;\n"
"  margin: 4px 2px;\n"
"border-radius: 12px;\n"
"transition-duration: 0.8s;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #525252;\n"
"    color: white;\n"
"}\n"
"\n"
"")
        self.deleteEntryButton.setObjectName("deleteEntryButton")
        self.dataTabMainLayoutV1.addWidget(self.deleteEntryButton)
        self.undoButton = QtWidgets.QPushButton(self.dataTab)
        self.undoButton.setStyleSheet("QPushButton{\n"
"    background-color: #e43f5a;\n"
"border: none;\n"
"  color: white;\n"
"  padding:10px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 12px;\n"
"  margin: 4px 2px;\n"
"border-radius: 12px;\n"
"transition-duration: 0.8s;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #525252;\n"
"    color: white;\n"
"}\n"
"\n"
"")
        self.undoButton.setObjectName("undoButton")
        self.dataTabMainLayoutV1.addWidget(self.undoButton)
        self.dataTabMainLayout.addLayout(self.dataTabMainLayoutV1)
        self.gridLayout_2.addLayout(self.dataTabMainLayout, 0, 1, 1, 1)
        self.tabWidget.addTab(self.dataTab, "")
        self.detectionTab = QtWidgets.QWidget()
        self.detectionTab.setObjectName("detectionTab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.detectionTab)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.label_3 = QtWidgets.QLabel(self.detectionTab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: #e43f5a;")
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.datasetComboBox = QtWidgets.QComboBox(self.detectionTab)
        self.datasetComboBox.setStyleSheet("background-color: #e43f5a;")
        self.datasetComboBox.setObjectName("datasetComboBox")
        self.verticalLayout_4.addWidget(self.datasetComboBox)

        self.addDatasetButton = QtWidgets.QPushButton(self.detectionTab)
        self.addDatasetButton.setStyleSheet("QPushButton{\n"
"    background-color: #e43f5a;\n"
"border: none;\n"
"  color: white;\n"
"  padding:10px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 12px;\n"
"  margin: 4px 2px;\n"
"border-radius: 12px;\n"
"transition-duration: 0.8s;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #525252;\n"
"    color: white;\n"
"}\n"
"\n"
"")
        self.addDatasetButton.setObjectName("addDatasetButton")
        self.verticalLayout_4.addWidget(self.addDatasetButton)

        spacerItem6 = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
       # self.verticalLayout_4.addItem(spacerItem6)
        self.verticalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout.addLayout(self.verticalLayout_5)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem7)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        #self.verticalLayout.addItem(spacerItem8)
        self.sc = MplCanvas(self, width=5, height=900, dpi=70)
        self.sc.axes.grid(True)
        self.verticalLayout.addWidget(self.sc)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem9)
        self.startButton = QtWidgets.QPushButton(self.detectionTab)
        self.startButton.setStyleSheet("QPushButton{\n"
"    background-color: #e43f5a;\n"
"border: none;\n"
"  color: white;\n"
"  padding:10px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 12px;\n"
"  margin: 4px 2px;\n"
"border-radius: 12px;\n"
"transition-duration: 0.8s;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #525252;\n"
"    color: white;\n"
"}\n"
"\n"
"")
        self.startButton.setObjectName("startButton")
        self.verticalLayout_3.addWidget(self.startButton)
        self.stopButton = QtWidgets.QPushButton(self.detectionTab)
        self.stopButton.setStyleSheet("QPushButton{\n"
"    background-color: #e43f5a;\n"
"border: none;\n"
"  color: white;\n"
"  padding:10px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 12px;\n"
"  margin: 4px 2px;\n"
"border-radius: 12px;\n"
"transition-duration: 0.8s;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #525252;\n"
"    color: white;\n"
"}\n"
"\n"
"")
        self.stopButton.setObjectName("stopButton")
        self.verticalLayout_3.addWidget(self.stopButton)
        self.label_4 = QtWidgets.QLabel(self.detectionTab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:#e43f5a;")
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.sampleSizeTextBox = QtWidgets.QLineEdit(self.detectionTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sampleSizeTextBox.sizePolicy().hasHeightForWidth())
        self.sampleSizeTextBox.setSizePolicy(sizePolicy)
        self.sampleSizeTextBox.setStyleSheet("background-color:#e43f5a")
        self.sampleSizeTextBox.setObjectName("sampleSizeTextBox")
        self.verticalLayout_3.addWidget(self.sampleSizeTextBox)
        self.duplicatesCheckbox = QtWidgets.QCheckBox(self.detectionTab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.duplicatesCheckbox.setFont(font)
        self.duplicatesCheckbox.setStyleSheet("color:#e43f5a;")
        self.duplicatesCheckbox.setObjectName("duplicatesCheckbox")
        self.verticalLayout_3.addWidget(self.duplicatesCheckbox)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem10)
        self.label_5 = QtWidgets.QLabel(self.detectionTab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color:#e43f5a;")
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.algorithmComboBox = QtWidgets.QComboBox(self.detectionTab)
        self.algorithmComboBox.setStyleSheet("background-color:#e43f5a;\n"
"")     
        self.algorithmComboBox.addItem("Naive (Exact Match)")
        self.algorithmComboBox.addItem("Levenshtein (Closest Match)")
        self.algorithmComboBox.addItem("Hamming (Closest Match)")
        self.algorithmComboBox.addItem("KMP (Partial Match)")
        self.algorithmComboBox.addItem("Rabin-Karp (Partial Match)")
        self.algorithmComboBox.setObjectName("algorithmComboBox")
        self.verticalLayout_3.addWidget(self.algorithmComboBox)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem11)
        self.speedTestButton = QtWidgets.QPushButton(self.detectionTab)
        self.speedTestButton.setStyleSheet("QPushButton{\n"
"    background-color: #e43f5a;\n"
"border: none;\n"
"  color: white;\n"
"  padding:10px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 12px;\n"
"  margin: 4px 2px;\n"
"border-radius: 12px;\n"
"transition-duration: 0.8s;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #525252;\n"
"    color: white;\n"
"}\n"
"\n"
"")
        self.speedTestButton.setObjectName("speedTestButton")
        self.verticalLayout_3.addWidget(self.speedTestButton)
        self.memoryTestButton = QtWidgets.QPushButton(self.detectionTab)
        self.memoryTestButton.setStyleSheet("QPushButton{\n"
"    background-color: #e43f5a;\n"
"border: none;\n"
"  color: white;\n"
"  padding:10px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 12px;\n"
"  margin: 4px 2px;\n"
"border-radius: 12px;\n"
"transition-duration: 0.8s;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #525252;\n"
"    color: white;\n"
"}\n"
"\n"
"")
        self.memoryTestButton.setObjectName("memoryTestButton")
        self.verticalLayout_3.addWidget(self.memoryTestButton)
        self.algorithmSpeedTestButton = QtWidgets.QPushButton(self.detectionTab)
        self.algorithmSpeedTestButton.setStyleSheet("QPushButton{\n"
"    background-color: #e43f5a;\n"
"border: none;\n"
"  color: white;\n"
"  padding:10px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 12px;\n"
"  margin: 4px 2px;\n"
"border-radius: 12px;\n"
"transition-duration: 0.8s;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #525252;\n"
"    color: white;\n"
"}")
        self.algorithmSpeedTestButton.setObjectName("algorithmSpeedTestButton")
        self.verticalLayout_3.addWidget(self.algorithmSpeedTestButton)
        self.algorithmMemoryComparisonButton = QtWidgets.QPushButton(self.detectionTab)
        self.algorithmMemoryComparisonButton.setStyleSheet("QPushButton{\n"
"    background-color: #e43f5a;\n"
"border: none;\n"
"  color: white;\n"
"  padding:10px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 12px;\n"
"  margin: 4px 2px;\n"
"border-radius: 12px;\n"
"transition-duration: 0.8s;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #525252;\n"
"    color: white;\n"
"}\n"
"")
        self.algorithmMemoryComparisonButton.setObjectName("algorithmMemoryComparisonButton")
        self.verticalLayout_3.addWidget(self.algorithmMemoryComparisonButton)
        spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem12)
        self.generateRandomDatasetButton_2 = QtWidgets.QPushButton(self.detectionTab)
        self.generateRandomDatasetButton_2.setStyleSheet("QPushButton{\n"
"    background-color: #e43f5a;\n"
"border: none;\n"
"  color: white;\n"
"  padding:10px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 12px;\n"
"  margin: 4px 2px;\n"
"border-radius: 12px;\n"
"transition-duration: 0.8s;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #525252;\n"
"    color: white;\n"
"}")
        self.generateRandomDatasetButton_2.setObjectName("generateRandomDatasetButton_2")
        self.verticalLayout_3.addWidget(self.generateRandomDatasetButton_2)
        self.label_6 = QtWidgets.QLabel(self.detectionTab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color:#e43f5a")
        self.label_6.setObjectName("label_6")
        self.verticalLayout_3.addWidget(self.label_6)
        self.randomSampleSizeTextBox = QtWidgets.QLineEdit(self.detectionTab)
        self.randomSampleSizeTextBox.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.randomSampleSizeTextBox.sizePolicy().hasHeightForWidth())
        self.randomSampleSizeTextBox.setSizePolicy(sizePolicy)
        self.randomSampleSizeTextBox.setStyleSheet("background-color:#e43f5a")
        self.randomSampleSizeTextBox.setObjectName("randomSampleSizeTextBox")
        self.verticalLayout_3.addWidget(self.randomSampleSizeTextBox)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.tabWidget.addTab(self.detectionTab, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1103, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.setupButtons()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Select a dataset to view, or to load onto the GPU. (Known malicious or test set)"))
        self.label.setText(_translate("MainWindow", "Search Dataset"))
        self.searchBar.setToolTip(_translate("MainWindow", "(Enter search term here)"))
        self.searchBar.setPlaceholderText(_translate("MainWindow", "Enter search term"))
        self.domainTable.setSortingEnabled(True)
        item = self.domainTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Domain"))
        __sortingEnabled = self.domainTable.isSortingEnabled()
        self.domainTable.setSortingEnabled(True)
        self.domainTable.setSortingEnabled(__sortingEnabled)
        self.addNewDatasetButton.setText(_translate("MainWindow", "Add New Dataset"))
        self.loadDataButton.setText(_translate("MainWindow", "Load Data Onto GPU"))
        self.generateRandomDatasetButton.setText(_translate("MainWindow", "Generate Random Dataset"))
        self.AppendDataButton.setText(_translate("MainWindow", "Append Data to Dataset"))
        self.nextPageButton.setText(_translate("MainWindow", "Next Page"))
        self.previousPageButton.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>QPushButton{</p><p>    background-color: #e43f5a;</p><p>border: none;</p><p>  color: white;</p><p>  padding:10px;</p><p>  text-align: center;</p><p>  text-decoration: none;</p><p>  display: inline-block;</p><p>  font-size: 12px;</p><p>  margin: 4px 2px;</p><p>border-radius: 12px;</p><p>transition-duration: 0.8s;</p><p>}</p><p><br/></p><p>QPushButton:hover {</p><p>    background-color: #525252;</p><p>    color: white;</p><p>}</p><p><br/></p><p><br/></p></body></html>"))
        self.previousPageButton.setText(_translate("MainWindow", "Previous Page"))
        self.label_7.setText(_translate("MainWindow", "Page:"))
        self.pageNumberLineEdit.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.goToPageButton.setText(_translate("MainWindow", "Go To Page"))
        self.addButton.setText(_translate("MainWindow", "Add Entry"))
        self.deleteEntryButton.setText(_translate("MainWindow", "Delete Entry"))
        self.undoButton.setText(_translate("MainWindow", "Undo"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.dataTab), _translate("MainWindow", "Data"))
        self.label_3.setText(_translate("MainWindow", "Select Dataset to be tested:"))
        self.startButton.setText(_translate("MainWindow", "Start Process"))
        self.stopButton.setText(_translate("MainWindow", "Stop Process"))
        self.label_4.setText(_translate("MainWindow", "Sample Size:"))
        self.duplicatesCheckbox.setText(_translate("MainWindow", "Duplicates"))
        self.label_5.setText(_translate("MainWindow", "Select Algorithm:"))
        self.speedTestButton.setText(_translate("MainWindow", "Speed Test"))
        self.memoryTestButton.setText(_translate("MainWindow", "Memory Test"))
        self.algorithmSpeedTestButton.setText(_translate("MainWindow", "Algorithm Speed Comparison Test"))
        self.algorithmMemoryComparisonButton.setText(_translate("MainWindow", "Algorithm Memory Comparison Test"))
        self.generateRandomDatasetButton_2.setText(_translate("MainWindow", "Generate Random Dataset"))
        self.label_6.setText(_translate("MainWindow", "Sample Size:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.detectionTab), _translate("MainWindow", "Detection"))
        self.addDatasetButton.setText(_translate("MainWindow", "Add Dataset"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())