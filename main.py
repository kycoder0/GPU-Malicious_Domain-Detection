#!/usr/bin/python3
# Author: Trevor Rice
# Date: Tue Jul 23 23:00:00 EDT 2019
# Purpose:
import os
directoryPath = os.path.dirname(os.path.realpath(__file__))
directoryPath = directoryPath[ :directoryPath.rfind('/')]
import sys
import subprocess
sys.path.insert(1, directoryPath + '/Code')
import MySQL.access as access
import DataProcessing.process as process
import CUDA.matcher as matcher
import pandas as pd
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import PyQt5.QtCore as QtCore
import CUDA.info as info
import RDG.generator as gen

#localdatapath = '/tmp/localdata.csv'

devices = info.Devices()

#db = "domains"

#matcher = matcher.Matcher(localdatapath)

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Malicious Domain Detection'
        self.left = 0
        self.top = 0
        self.width = 850
        self.height = 700
        self.setWindowTitle(self.title)
        #self.setFixedSize(self.width, self.height)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("""
            QMainWindow {
                background: #2F394D;
            }
        """)
        self.table_widget = TableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()


class Button():
    def __init__(self, text, size, position, groupBox, layout):
        self.button = QPushButton(groupBox)
        self.button.setText(text)
        self.button.resize(size[0], size[1])
        self.button.move(position[0], position[1])
        layout.addWidget(self.button)

class Console:
    def __init__(self, position, size, parent):
        self.console_box = QVBoxLayout()
        spacer = QSpacerItem(290, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)
        #self.console_box.addItem(spacer)
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.move(position[0], position[1])
        self.console.resize(size[0], size[1])
        self.console_box.addWidget(self.console)
        parent.setLayout(self.console_box)

class TableWidget(QWidget):

    class DataTab(QWidget):

        def __init__(self, parent):
            super(QWidget, self).__init__(parent)
            # main layout is VBox
            self.mainLayout = QVBoxLayout()

            # group box for data
            self.dataVBox = QVBoxLayout()
            # group box for console output
            self.consoleVBox = QVBoxLayout()
            # adding group boxes to the main layout
            self.mainLayout.addLayout(self.dataVBox)
            self.mainLayout.addLayout(self.consoleVBox)

            #self.dataGroupBox.setLayout(self.dataVBox)
            self.buttonGroupBox = QGroupBox()
            addData = Button("Add data", [190, 40], [40, 40], self.buttonGroupBox, self.dataVBox)
            spacer = QSpacerItem(290, 100, QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.dataVBox.addItem(spacer)
            
            self.consoleGroupBox = QGroupBox("Console Output")
            spacer = QSpacerItem(290, 100, QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.dataVBox.addItem(spacer)
            self.console = Console([100, 20], [50, 50], self.consoleGroupBox)
            self.consoleVBox.addWidget(self.consoleGroupBox)

            self.mainLayout.addLayout(self.dataVBox)
            spacer2 = QSpacerItem(290, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.mainLayout.addItem(spacer2)
            self.mainLayout.addStretch()
            self.mainLayout.addLayout(self.consoleVBox)
            self.setLayout(self.mainLayout)


    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.loaded_test_data = None
        self.sample_test_data = None
        ############################################
        #                                          #
        #            Initialize Tabs               #
        #                                          #
        ############################################
        self.tabs = QTabWidget()
        self.data_tab = self.DataTab(self)
        self.detection_tab = QWidget()
        self.gpu_tab = QWidget()
        self.about_tab = QWidget()
        self.tabs.resize(300,200)
        #e8ad9f
        self.setStyleSheet("""
            QVBoxLayout {
                background-color: red;
            }
            QWidget {

                background:#494949;
            }
            QLineEdit {
                background: white;
            }
            QLineEdit:disabled {
                background: #CDCDCD;
            }
            QLabel {
                color: black;
            }
            QPushButton {
                background-color: #33658A;
                color: black;
            }
            QPushButton:disabled {
                background-color: white;
            }
            QPushButton:hover {
                color:#4C151E;
            }
            QTextEdit {
                background: #e8ad9f;
                color: black;
            }
            QSpacerItem {
                border: 5px solid red;
            }
        """)

        


        # adding tabs to the window
        self.tabs.addTab(self.data_tab,"Data/Database")
        self.tabs.addTab(self.gpu_tab,"GPU Info")
        self.tabs.addTab(self.about_tab,"About")




        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def run_with(self):
        if self.cpu_radio.isChecked():
            if self.gpu_radio.isChecked():
                return 2
            return 1
        return 0

    def parse_column_num(self):
        try:
            return int(self.column_text.text())
        except ValueError:
            self.console_write("Invalid entry for Column #", True)
            return -1

    def parse_num_samples(self):
        try:
            return int(self.num_samples.text())
        except ValueError:
            self.console_write("Invalid entry for # Samples", True)
            return -1
    def gui_visible(self, visible):
        self.data_tab.group_box_database.setEnabled(visible)
        self.data_tab.group_box_detection.setEnabled(visible)
        QtCore.QCoreApplication.processEvents()
        QtCore.QCoreApplication.flush()

    def console_write(self, line, newline):
        self.console.moveCursor(QTextCursor.End)
        self.console.insertPlainText(line)
        if newline:
            self.console.append("> ")
        self.console.moveCursor(QTextCursor.End)
        QtCore.QCoreApplication.processEvents()
        QtCore.QCoreApplication.flush()

    def console_append(self, line):
        self.console.append("   $ " + line)
        self.console.moveCursor(QTextCursor.End)
        QtCore.QCoreApplication.processEvents()
        QtCore.QCoreApplication.flush()


    def search_enable(self, enable):
        self.search_button.setEnabled(enable)
        self.speed_test_button.setEnabled(enable)
        # self.memory_test_button.setEnabled(enable)
        QtCore.QCoreApplication.processEvents()
        QtCore.QCoreApplication.flush()

    def test_enable(self, enable):
        self.num_samples.setEnabled(enable)
        self.column_text.setEnabled(enable)
        self.load_test_data.setEnabled(enable)
        QtCore.QCoreApplication.processEvents()
        QtCore.QCoreApplication.flush()

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    def addDataFromFile(self):
        self.gui_visible(False)

        self.console.moveCursor(QTextCursor.End)

        file = QFileDialog.getOpenFileName(self, "Choose Data", "", "csv(*.csv)")
        if "csv" in file[0]:
            self.console_write("Adding Data from " + file[0] + "...", False)
            self.console.moveCursor(QTextCursor.End)
            process.insert_data(file[0], 10000, database, 'Connection')
            database.to_csv('Connection', localdatapath)
            self.console_append("Finished adding data")
            self.console_write("", True)
        else:
            self.console_write("Please select a valid .csv file", True)
        self.console.moveCursor(QTextCursor.End)
        self.gui_visible(True)

    def refreshLocalRepository(self):
        self.gui_visible(False)
        self.console_write("Refreshing Data...", False)
        database.to_csv('Connection', localdatapath)
        self.console_append("Finished refreshing data")
        self.console_write("", True)
        self.gui_visible(True)

    def scrape(self):
        self.console_write("Scraping", True)
        pass

    def gpu_clicked(self):
        if not self.gpu_radio.isChecked() and not self.cpu_radio.isChecked():
            self.cpu_radio.setChecked(True)
        if self.gpu_radio.isChecked():
            self.load_data.setEnabled(True)
        else:
            self.load_data.setEnabled(False)
            self.unload_data.setEnabled(False)


    def cpu_clicked(self):
        if not self.gpu_radio.isChecked() and not self.cpu_radio.isChecked():
            self.gpu_radio.setChecked(True)

    def load_data_gpu(self):
        self.console_write("Loading data onto GPU...", False)
        self.gui_visible(False)
        self.load_data.setEnabled(False)
        self.unload_data.setEnabled(True)
        matcher.load_gpu()
        self.console_append("Data loaded onto GPU successfully")
        self.console_write("", True)
        self.gui_visible(True)

    def unload_data_gpu(self):
        self.console_write("Unloading data from GPU...", False)
        self.load_data.setEnabled(True)
        self.unload_data.setEnabled(False)
        matcher.unload_gpu()
        self.console_append("Unloaded data from GPU successfully")
        self.console_write("", True)

    def choose_data_file(self):
        self.gui_visible(False)
        file = QFileDialog.getOpenFileName(self, "Choose Data", "", "csv(*.csv)")
        if len(file[0]) > 0:
            self.data_file.setText(file[0])
            if os.path.exists(self.data_file.text()):
                self.console_write("Loading test data from " + self.data_file.text(), False)
                self.loaded_test_data = pd.read_csv(self.data_file.text(), encoding = "ISO-8859-1", sep = ',', dtype='unicode', header = None)
                self.console_append("Loaded test data successfully")
                self.console_write("", True)
                self.test_enable(True)
            else:
                self.console_write("Invalid file")
        self.load_test_data.setEnabled(True)
        self.gui_visible(True)
        self.console_write("Head: \n" + self.loaded_test_data.head().to_string(), True)

    def search(self):

        what_device = self.run_with()
        if what_device == 1:
            self.gui_visible(False)
            self.console_write("Searching with CPU", False)
            num_matches = matcher.cpu_run(self.sample_test_data)
            self.console_append(str(num_matches) + " malicious domains detected with CPU")
            self.console_write("", True)
        else:
            if self.load_data.isEnabled():
                self.console_write("Please load data onto the GPU", True)
            else:
                self.gui_visible(False)
                if what_device == 2:
                    self.console_write("Searching with CPU and GPU", False)
                    self.console_append("Searching with GPU")
                    num_matches = matcher.gpu_run(self.sample_test_data)
                    self.console_append(str(num_matches) + " malicious domains detected with GPU")
                    self.console_append("Searching with CPU")
                    num_matches = matcher.cpu_run(self.sample_test_data)
                    self.console_append(str(num_matches) + " malicious domains detected with CPU")
                    self.console_write("", True)

                else:
                    self.console_write("Searching with GPU", False)
                    num_matches = matcher.gpu_run(self.sample_test_data)
                    self.console_append(str(num_matches) + " malicious domains detected with GPU")
                    self.console_write("", True)
        self.gui_visible(True)

    def speed_test(self):
        what_device = self.run_with()
        if what_device == 1:
            self.gui_visible(False)
            self.console_write("Speed Test with CPU", False)
            speed_data = matcher.cpu_speed_test(self.sample_test_data)
            self.console_append(str(speed_data[0]) + " malicious domains detected with CPU")
            self.console_append("Samples tested: " + str(len(self.sample_test_data)))
            self.console_append("Total time: " + str(speed_data[1]) + " seconds")
            self.console_write("", True)
        else:
            if self.load_data.isEnabled():
                self.console_write("Please load data onto the GPU", True)
            else:
                self.gui_visible(False)
                if what_device == 2:
                    self.console_write("Speed Test with CPU and GPU", False)
                    speed_data = matcher.gpu_speed_test(self.sample_test_data)
                    gpu_time = speed_data[1]
                    speed_data = matcher.cpu_speed_test(self.sample_test_data)
                    cpu_time = speed_data[1]
                    self.console_append(str(speed_data[0]) + " malicious domains detected")
                    self.console_append("Samples tested: " + str(len(self.sample_test_data)))
                    self.console_append("CPU time: " + str(cpu_time))
                    self.console_append("GPU time: " + str(gpu_time))
                    if (cpu_time > gpu_time):
                        self.console_append("The GPU ran " + str(cpu_time-gpu_time) + " seconds faster than the CPU")
                    else:
                        self.console_append("The CPU ran " + str(gpu_time-cpu_time) + " seconds faster than the GPU")
                    self.console_write("", True)

                else:
                    self.console_write("Speed Test with GPU", False)
                    speed_data = matcher.gpu_speed_test(self.sample_test_data)
                    self.console_append(str(speed_data[0]) + " malicious domains detected with GPU")
                    self.console_append("Samples tested: " + str(len(self.sample_test_data)))
                    self.console_append("Total time: " + str(speed_data[1]) + " seconds")
                    self.console_write("", True)
        self.gui_visible(True)
    def memory_test(self):
        what_device = self.run_with()
        if what_device == 1:
            self.gui_visible(False)
            self.console_write("Memory Test with CPU", False)
            matcher.cpu_memory_test(self.sample_test_data)
            # speed_data = matcher.cpu_memory_test(self.sample_test_data)
            # self.console_append(str(speed_data[0]) + " malicious domains detected with CPU")
            # self.console_append("Samples tested: " + str(len(self.sample_test_data)))
            # self.console_append("Total time: " + str(speed_data[1]) + " seconds")
            self.console_write("", True)
        else:
            if self.load_data.isEnabled():
                self.console_write("Please load data onto the GPU", True)
            else:
                self.gui_visible(False)
                if what_device == 2:
                    self.console_write("Speed Test with CPU and GPU", False)
                    speed_data = matcher.gpu_speed_test(self.sample_test_data)
                    gpu_time = speed_data[1]
                    speed_data = matcher.cpu_speed_test(self.sample_test_data)
                    cpu_time = speed_data[1]
                    self.console_append(str(speed_data[0]) + " malicious domains detected")
                    self.console_append("Samples tested: " + str(len(self.sample_test_data)))
                    self.console_append("CPU time: " + str(cpu_time))
                    self.console_append("GPU time: " + str(gpu_time))
                    if (cpu_time > gpu_time):
                        self.console_append("The GPU ran " + str(cpu_time-gpu_time) + " seconds faster than the CPU")
                    else:
                        self.console_append("The CPU ran " + str(gpu_time-cpu_time) + " seconds faster than the GPU")
                    self.console_write("", True)

                else:
                    self.console_write("Speed Test with GPU", False)
                    speed_data = matcher.gpu_speed_test(self.sample_test_data)
                    self.console_append(str(speed_data[0]) + " malicious domains detected with GPU")
                    self.console_append("Samples tested: " + str(len(self.sample_test_data)))
                    self.console_append("Total time: " + str(speed_data[1]) + " seconds")
                    self.console_write("", True)
        self.gui_visible(True)

    def load_sample_test_data(self):

        column_num = self.parse_column_num()
        num_samples = self.parse_num_samples()
        if num_samples <= 0:
            self.console_write("Enter samples greater than 0", True)
        else:

            if 0 <= column_num < len(self.loaded_test_data.columns):
                self.console_write("Loading sample data...", False)
                self.sample_test_data = self.loaded_test_data[self.loaded_test_data.columns[column_num]]
                self.sample_test_data = self.sample_test_data.to_frame()
                self.sample_test_data = process.get_sample(self.sample_test_data, num_samples)
                self.console_append("Successfully loaded sample data!")
                self.console_write("", True)
                self.search_enable(True)
            else:
                self.console_write("Enter a valid column number", True)

    def generate_random_data(self):
        self.console_write("Generating random data", False)
        size = 0
        try:
            size = int(self.random_data_size.text())
        except ValueError:
            self.console_append("Invalid size for random data generation")
            self.console_write("", True)
            return
        if size <= 0:
            self.console_append("Enter a size greater than 0")
            return
        gen.Generator.generate(size)
        self.console_append("Number of domains: " + str(size))
        self.console_append("Data stored at " + directoryPath + '/Data/random.csv')
        self.console_write("", True)


    def on_combo_changed(self, value):
        self.gpu_tab.data_textbox.setText(devices.get_info(int(value)))

if __name__ == '__main__':
    #database = access.Connection("localhost", "root", "", "domains", False)
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())