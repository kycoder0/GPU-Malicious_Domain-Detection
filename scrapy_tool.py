# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scrapy.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

from bs4 import BeautifulSoup
from subprocess import call
import os
import pickle
import json
class Ui_ScrapyTool(object):


    def dumpQuery(self):
        data = {}
        data['flags'] = []
        data['flags'].append({
            'name': 'CSS',
            'status': self.cssRadioButton.isChecked()
        })
        data['flags'].append({
            'name': 'XPath',
            'status': self.xPathRadioButton.isChecked()
        })
        data['flags'].append({
            'name': 'Function',
            'status': self.useFunctionCheckBox.isChecked()
        })

        data['flags'].append({
            'name': 'Regex',
            'status': self.useRegexCheckBox.isChecked()
        })

        data['text'] = []

        data['text'].append({
            'type': 'Query',
            'raw': self.queryTextEdit.toPlainText()
        })
        data['text'].append({
            'type': 'Function',
            'raw': self.functionTextEdit.toPlainText()
        })
        data['text'].append({
            'type': 'Regex',
            'raw': self.regexTextEdit.toPlainText()
        })

        data['url'] = self.urlLineEdit.text()
        with open('domains\\querySettings.json', 'w+') as outfile:
            json.dump(data, outfile)
    def urlSearchButtonClicked(self):
        import urllib.request
        url = self.urlLineEdit.text()
        try:
            fp = urllib.request.urlopen(url)
        except:
            print('Invalid URL')
            return
        mybytes = fp.read()
        mystr = mybytes.decode(fp.headers.get_content_charset())
        fp.close()
        soup = BeautifulSoup(mystr, 'html.parser')

        self.htmlText.insertPlainText(soup.prettify())
    def runQueryButtonClicked(self):
        self.dumpQuery()
        name = "domains"
        call(["scrapy", "crawl", "{0}".format(name), "-o {0}.json".format(name)])
        result = pickle.load(open('output.txt', 'rb'))
        self.resultsTable.setRowCount(0)
        self.resultsTable.setRowCount(len(result))
        self.resultsTable.setColumnCount(1)
        for index, item in enumerate(result):
            self.resultsTable.setItem(index, 0, QtWidgets.QTableWidgetItem(result[index]))
        with open('output.csv', 'w') as out:
            for item in result:
                out.write(str(item)+'\n')
    def cssRadioButtonToggled(self):
        print('henlo')
    def xPathRadioButtonToggled(self):
        print('henlo')
    def useFunctionCheckBoxChanged(self):
        print('henlo')
    def useRegexCheckBoxChanged(self):
        print('henlo')

    def setupOnClicks(self):
        self.urlSearchButton.clicked.connect(self.urlSearchButtonClicked)
        self.runQueryButton.clicked.connect(self.runQueryButtonClicked)
        self.cssRadioButton.toggled.connect(self.cssRadioButtonToggled)
        self.xPathRadioButton.toggled.connect(self.xPathRadioButtonToggled)
        self.useFunctionCheckBox.stateChanged.connect(self.useFunctionCheckBoxChanged)
        self.useRegexCheckBox.stateChanged.connect(self.useRegexCheckBoxChanged)

    def setupUi(self, ScrapyTool):
        cwd = os.getcwd() + '\\'
        os.chdir(cwd + 'domains')
        ScrapyTool.setObjectName("ScrapyTool")
        ScrapyTool.resize(800, 600)
        self.gridLayout = QtWidgets.QGridLayout(ScrapyTool)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(ScrapyTool)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.urlLineEdit = QtWidgets.QLineEdit(self.tab)
        self.urlLineEdit.setObjectName("urlLineEdit")
        self.horizontalLayout.addWidget(self.urlLineEdit)
        self.urlSearchButton = QtWidgets.QPushButton(self.tab)
        self.urlSearchButton.setObjectName("urlSearchButton")
        self.horizontalLayout.addWidget(self.urlSearchButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.htmlText = QtWidgets.QTextEdit(self.tab)
        self.htmlText.setReadOnly(True)
        self.htmlText.setObjectName("htmlText")
        self.verticalLayout.addWidget(self.htmlText)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_2 = QtWidgets.QLabel(self.tab_3)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_6.addWidget(self.label_2)
        self.cssRadioButton = QtWidgets.QRadioButton(self.tab_3)
        self.cssRadioButton.setChecked(True)
        self.cssRadioButton.setObjectName("cssRadioButton")
        self.verticalLayout_6.addWidget(self.cssRadioButton)
        self.xPathRadioButton = QtWidgets.QRadioButton(self.tab_3)
        self.xPathRadioButton.setObjectName("xPathRadioButton")
        self.verticalLayout_6.addWidget(self.xPathRadioButton)
        self.queryTextEdit = QtWidgets.QTextEdit(self.tab_3)
        self.queryTextEdit.setObjectName("queryTextEdit")
        self.verticalLayout_6.addWidget(self.queryTextEdit)
        self.verticalLayout_4.addLayout(self.verticalLayout_6)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_4.addLayout(self.verticalLayout_7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_4 = QtWidgets.QLabel(self.tab_3)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.useRegexCheckBox = QtWidgets.QCheckBox(self.tab_3)
        self.useRegexCheckBox.setObjectName("useRegexCheckBox")
        self.horizontalLayout_6.addWidget(self.useRegexCheckBox)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.regexTextEdit = QtWidgets.QTextEdit(self.tab_3)
        self.regexTextEdit.setObjectName("regexTextEdit")
        self.verticalLayout_4.addWidget(self.regexTextEdit)
        self.runQueryButton = QtWidgets.QPushButton(self.tab_3)
        self.runQueryButton.setObjectName("runQueryButton")
        self.verticalLayout_4.addWidget(self.runQueryButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.tab_3)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.useFunctionCheckBox = QtWidgets.QCheckBox(self.tab_3)
        self.useFunctionCheckBox.setObjectName("useFunctionCheckBox")
        self.horizontalLayout_3.addWidget(self.useFunctionCheckBox)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.functionTextEdit = QtWidgets.QTextEdit(self.tab_3)
        self.functionTextEdit.setObjectName("functionTextEdit")
        self.verticalLayout_5.addWidget(self.functionTextEdit)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.gridLayout_3.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.resultsTable = QtWidgets.QTableWidget(self.tab_3)
        self.resultsTable.setObjectName("resultsTable")
        self.resultsTable.setColumnCount(0)
        self.resultsTable.setRowCount(0)
        self.gridLayout_3.addWidget(self.resultsTable, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.tab_3)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(ScrapyTool)
        self.tabWidget.setCurrentIndex(0)
        self.setupOnClicks()
        self.functionTextEdit.insertPlainText('''def extra_python(result): # you must have this function
    return result''')
        QtCore.QMetaObject.connectSlotsByName(ScrapyTool)

    def retranslateUi(self, ScrapyTool):
        _translate = QtCore.QCoreApplication.translate
        ScrapyTool.setWindowTitle(_translate("ScrapyTool", "Scrapy Tool"))
        self.label.setText(_translate("ScrapyTool", "Enter Url:"))
        self.urlSearchButton.setText(_translate("ScrapyTool", "Search"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("ScrapyTool", "Source"))
        self.label_2.setText(_translate("ScrapyTool", "Query"))
        self.cssRadioButton.setText(_translate("ScrapyTool", "CSS"))
        self.xPathRadioButton.setText(_translate("ScrapyTool", "XPath"))
        self.label_4.setText(_translate("ScrapyTool", "Regex"))
        self.useRegexCheckBox.setText(_translate("ScrapyTool", "Use Regex"))
        self.runQueryButton.setText(_translate("ScrapyTool", "Run Query"))
        self.label_3.setText(_translate("ScrapyTool", "Function"))
        self.useFunctionCheckBox.setText(_translate("ScrapyTool", "Use Function"))
        self.label_5.setText(_translate("ScrapyTool", "Results:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("ScrapyTool", "Tools"))


# if __name__ == "__main__":
#     import sys
   
#     app = QtWidgets.QApplication(sys.argv)
#     ScrapyTool = QtWidgets.QWidget()
#     ui = Ui_ScrapyTool()
#     ui.setupUi(ScrapyTool)
#     ScrapyTool.show()
#     sys.exit(app.exec_())
