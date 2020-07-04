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


class Ui_MainWindow(object):

    def insertDataToDomainTable(self, data):
        for i in range(len(data)):
            self.domainTable.insertRow(i)
            for j in range(3):
                self.domainTable.setItem(i, j, QtWidgets.QTableWidgetItem(str(data[j][i])))
    def updateTableView(self, dataFilePath):
        if os.path.exists(dataFilePath):
            data = pd.read_csv(dataFilePath, encoding = "ISO-8859-1", sep = ',', dtype='unicode', header = None)
            print(data[0], data[1])
            thread = Thread(target = self.insertDataToDomainTable, args = (data, ))
            thread.start()
            
    def addNewDatasetClick(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, "Choose Data", "", "csv(*.csv)")
        self.maliciousDatasetComboBox.addItem(file[0])
        if '.csv' in file[1]:
            self.updateTableView(file[0])
        print(file)
    def setupUi(self, MainWindow):
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
"    background-color: #bb86fc;\n"
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
"QTabWidget::pane { border: 0; }")
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
"    background-color: #bb86fc;\n"
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
"    background-color: #bb86fc;\n"
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
        self.label_2.setStyleSheet("color: #bb86fc;")
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.maliciousDatasetComboBox = QtWidgets.QComboBox(self.dataTab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.maliciousDatasetComboBox.setFont(font)
        self.maliciousDatasetComboBox.setStyleSheet("background-color: #bb86fc;")
        self.maliciousDatasetComboBox.setObjectName("maliciousDatasetComboBox")
        self.gridLayout_3.addWidget(self.maliciousDatasetComboBox, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.dataTab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #bb86fc;\n"
"font-size: 12;")
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 3, 0, 1, 1)
        self.searchBar = QtWidgets.QLineEdit(self.dataTab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.searchBar.setFont(font)
        self.searchBar.setStatusTip("")
        self.searchBar.setStyleSheet("background-color: #bb86fc;\n"
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
        self.domainTable.setStyleSheet("background-color: #525252; color: #bb86fc; font-weight: bold;")
        self.domainTable.setShowGrid(True)
        self.domainTable.setCornerButtonEnabled(False)
        self.domainTable.setObjectName("domainTable")
        self.domainTable.setColumnCount(3)
        self.domainTable.setRowCount(37)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(17, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(18, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(19, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(20, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(21, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(22, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(23, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(24, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(25, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(26, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(27, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(28, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(29, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(30, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(31, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(32, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(33, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(34, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(35, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setVerticalHeaderItem(36, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.domainTable.setItem(0, 2, item)

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
"    background-color: #bb86fc;\n"
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
"    background-color: #bb86fc;\n"
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
"    background-color: #bb86fc;\n"
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
"    background-color: #bb86fc;\n"
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
        self.addButton = QtWidgets.QPushButton(self.dataTab)
        self.addButton.setStyleSheet("QPushButton{\n"
"    background-color: #bb86fc;\n"
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
"    background-color: #bb86fc;\n"
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
"    background-color: #bb86fc;\n"
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
        self.label_3.setStyleSheet("color: #bb86fc;")
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.datasetComboBox = QtWidgets.QComboBox(self.detectionTab)
        self.datasetComboBox.setStyleSheet("background-color: #bb86fc;")
        self.datasetComboBox.setObjectName("datasetComboBox")
        self.verticalLayout_4.addWidget(self.datasetComboBox)
        spacerItem3 = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_4.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout.addLayout(self.verticalLayout_5)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem5)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem6)
        self.startButton = QtWidgets.QPushButton(self.detectionTab)
        self.startButton.setStyleSheet("QPushButton{\n"
"    background-color: #bb86fc;\n"
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
"    background-color: #bb86fc;\n"
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
        self.label_4.setStyleSheet("color:#bb86fc;")
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.sampleSizeTextBox = QtWidgets.QLineEdit(self.detectionTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sampleSizeTextBox.sizePolicy().hasHeightForWidth())
        self.sampleSizeTextBox.setSizePolicy(sizePolicy)
        self.sampleSizeTextBox.setStyleSheet("background-color:#bb86fc")
        self.sampleSizeTextBox.setObjectName("sampleSizeTextBox")
        self.verticalLayout_3.addWidget(self.sampleSizeTextBox)
        self.duplicatesCheckbox = QtWidgets.QCheckBox(self.detectionTab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.duplicatesCheckbox.setFont(font)
        self.duplicatesCheckbox.setStyleSheet("color:#bb86fc;")
        self.duplicatesCheckbox.setObjectName("duplicatesCheckbox")
        self.verticalLayout_3.addWidget(self.duplicatesCheckbox)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem7)
        self.label_5 = QtWidgets.QLabel(self.detectionTab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color:#bb86fc;")
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.algorithmComboBox = QtWidgets.QComboBox(self.detectionTab)
        self.algorithmComboBox.setStyleSheet("background-color:#bb86fc;\n"
"")
        self.algorithmComboBox.setObjectName("algorithmComboBox")
        self.verticalLayout_3.addWidget(self.algorithmComboBox)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem8)
        self.speedTestButton = QtWidgets.QPushButton(self.detectionTab)
        self.speedTestButton.setStyleSheet("QPushButton{\n"
"    background-color: #bb86fc;\n"
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
"    background-color: #bb86fc;\n"
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
"    background-color: #bb86fc;\n"
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
"    background-color: #bb86fc;\n"
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
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem9)
        self.generateRandomDatasetButton_2 = QtWidgets.QPushButton(self.detectionTab)
        self.generateRandomDatasetButton_2.setStyleSheet("QPushButton{\n"
"    background-color: #bb86fc;\n"
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
        self.label_6.setStyleSheet("color:#bb86fc")
        self.label_6.setObjectName("label_6")
        self.verticalLayout_3.addWidget(self.label_6)
        self.randomSampleSizeTextBox = QtWidgets.QLineEdit(self.detectionTab)
        self.randomSampleSizeTextBox.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.randomSampleSizeTextBox.sizePolicy().hasHeightForWidth())
        self.randomSampleSizeTextBox.setSizePolicy(sizePolicy)
        self.randomSampleSizeTextBox.setStyleSheet("background-color:#bb86fc")
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
        self.tabWidget.setCurrentIndex(1)

        # hook up clicks
        self.addNewDatasetButton.clicked.connect(self.addNewDatasetClick)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Select a dataset to view, or to load onto the GPU. (Known malicious or test set)"))
        self.maliciousDatasetComboBox.setItemText(0, _translate("MainWindow", "New Item"))
        self.maliciousDatasetComboBox.setItemText(1, _translate("MainWindow", "New Item"))
        self.maliciousDatasetComboBox.setItemText(2, _translate("MainWindow", "New Item"))
        self.maliciousDatasetComboBox.setItemText(3, _translate("MainWindow", "New Item"))
        self.label.setText(_translate("MainWindow", "Search Dataset"))
        self.searchBar.setToolTip(_translate("MainWindow", "(Enter search term here)"))
        self.searchBar.setPlaceholderText(_translate("MainWindow", "Enter search term"))
        self.domainTable.setSortingEnabled(True)
  
        item = self.domainTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Static IP"))
        item = self.domainTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Domain"))
        item = self.domainTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Timestamp"))
        __sortingEnabled = self.domainTable.isSortingEnabled()
        self.domainTable.setSortingEnabled(True)
        self.domainTable.setSortingEnabled(__sortingEnabled)
        self.addNewDatasetButton.setText(_translate("MainWindow", "Add New Dataset"))
        self.loadDataButton.setText(_translate("MainWindow", "Load Data Onto GPU"))
        self.generateRandomDatasetButton.setText(_translate("MainWindow", "Generate Random Dataset"))
        self.AppendDataButton.setText(_translate("MainWindow", "Append Data to Dataset"))
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
