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

localdatapath = '/tmp/localdata.csv'

devices = info.Devices()

db = "domains"

matcher = matcher.Matcher(localdatapath)

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Malicious Domain Detection'
        self.left = 0
        self.top = 0
        self.width = 850
        self.height = 700
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("""
            QMainWindow {
                background: #4C151E;
            }
        """)
        self.table_widget = TableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()

class TableWidget(QWidget):

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
        self.data_tab = QWidget()
        self.detection_tab = QWidget()
        self.gpu_tab = QWidget()
        self.about_tab = QWidget()
        self.tabs.resize(300,200)
        #e8ad9f
        self.setStyleSheet("""
            QWidget {

                background:#e18478;
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
                background-color: #992c3e;
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
        """)
        ########################################################################

        ############################################
        #                                          #
        #                Add Tabs                  #
        #                                          #
        ############################################
        self.tabs.addTab(self.data_tab,"Data and Detection")
        self.tabs.addTab(self.gpu_tab,"GPU Info")
        self.tabs.addTab(self.about_tab,"About")
        ########################################################################

        ############################################
        #                                          #
        #          Data and Detection Tab          #
        #                                          #
        ############################################
        self.data_tab.grid = QVBoxLayout()
        self.data_tab.setLayout(self.data_tab.grid)
        self.data_tab.group_box_database = QGroupBox("Database and Scrapy")
        self.data_tab.group_box_detection = QGroupBox("Detection")
        self.data_tab.group_box_console = QGroupBox("Console")

        self.data_tab.grid.addWidget(self.data_tab.group_box_database)
        self.data_tab.grid.addWidget(self.data_tab.group_box_detection)
        self.data_tab.grid.addWidget(self.data_tab.group_box_console)

        ##### Database and Scrapy Box
        database_box = QVBoxLayout()
        addData = QPushButton(self.data_tab.group_box_database)
        addData.setText("Add Data")
        addData.resize(190, 40)
        addData.move(40, 40)

        addData.clicked.connect(self.addDataFromFile)

        refreshLocal = QPushButton(self.data_tab.group_box_database)
        refreshLocal.setText("Refresh Local Data")
        refreshLocal.resize(190, 40)
        refreshLocal.move(40, 120)
        refreshLocal.clicked.connect(self.refreshLocalRepository)

        databaseLabel = QLabel(self.data_tab.group_box_database)
        databaseLabel.move(250, 25)
        databaseLabel.resize(300, 150)
        databaseLabel.setWordWrap(True)
        databaseLabel.setText("Use this section to manage domain data. Push the Add Data button to select a valid csv file to insert into our database. The file must be in the format of (0. Static IP, 2. Domain, 4. Time Stamp). Refresh Local Data will download the data from our database to a local file /tmp/localdata.csv. Scrape Data will allow you to scrape data from a given url and process it into the specified format.")

        scrape = QPushButton(self.data_tab.group_box_database)
        scrape.setText("Scrape Data")
        scrape.resize(190, 40)
        scrape.move(580, 80)
        scrape.clicked.connect(self.scrape)

        verticalSpacer1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        database_box.addItem(verticalSpacer1)

        ############### Detection Box ##########################################
        detection_box = QVBoxLayout()
        #detection_box.addStretch(0)
        self.cpu_radio = QCheckBox("CPU")
        self.cpu_radio.setChecked(True)
        self.cpu_radio.toggled.connect(self.cpu_clicked)
        self.cpu_radio.setMaximumSize(50, 20)
        detection_box.addWidget(self.cpu_radio)
        self.cpu_radio.setStyleSheet("""

            QCheckBox {
                color: black;
            }
            """)
        self.gpu_radio = QCheckBox("GPU")
        self.gpu_radio.setChecked(False)
        self.gpu_radio.toggled.connect(self.gpu_clicked)
        self.gpu_radio.setLayoutDirection(0)
        self.gpu_radio.setMaximumSize(50, 20)
        self.gpu_radio.resize(30, 20)
        detection_box.addWidget(self.gpu_radio)


        #self.cpu_gpu_box = QGroupBox("Select")



        #detection_box.addWidget(self.cpu_gpu_box)
        ############### Load Data Button ######################################
        self.load_data = QPushButton(self.data_tab.group_box_detection)
        self.load_data.setText("Load Data (GPU)")
        self.load_data.setObjectName("loadGPUData")
        self.load_data.setEnabled(False)
        self.load_data.resize(130, 30)
        self.load_data.move(20, 100)
        self.load_data.clicked.connect(self.load_data_gpu)

        self.load_data.setStyleSheet("""
            QPushButton {
                background: #98FB98;
            }
            QPushButton:disabled {
                background: #98FB98;
            }
        """)
        ########################################################################


        ############### Unload Data Button #####################################
        self.unload_data = QPushButton(self.data_tab.group_box_detection)
        self.unload_data.setText("Unload Data (GPU)")
        self.unload_data.setEnabled(False)
        self.unload_data.resize(130, 30)
        self.unload_data.move(20, 150)
        self.unload_data.clicked.connect(self.unload_data_gpu)
        self.unload_data.setStyleSheet("""
            QPushButton {
                background: #98FB98;
            }
            QPushButton:disabled {
                background: #98FB98;
            }
        """)
        ############### Manual Search Button/Text ##############################
        # self.manual_search = QPushButton(self.data_tab.group_box_detection)
        # self.manual_search.setText("Manual Search")
        # self.manual_search.resize(130, 30)
        # self.manual_search.move(170, 50)
        # #self.manual_search.clicked.connect(self.load_data_gpu)
        #
        # self.manual_search_file = QLineEdit(self.data_tab.group_box_detection)
        # self.manual_search_file.resize(300, 25)
        # self.manual_search_file.move(330, 52)
        ########################################################################

        ############### Search/Testing Buttons and File QLineEdit ##############
        self.file_label = QLabel(self.data_tab.group_box_detection)
        self.file_label.setText("Select File: ")
        self.file_label.resize(120, 20)
        self.file_label.move(185, 32)

        self.data_file = QLineEdit(self.data_tab.group_box_detection)
        self.data_file.setReadOnly(True)
        self.data_file.resize(400, 25)
        self.data_file.move(275, 32)


        self.choose_data_button = QPushButton(self.data_tab.group_box_detection)
        self.choose_data_button.resize(25, 25)
        self.choose_data_button.move(680, 32)
        self.choose_data_button.setText("...")
        self.choose_data_button.clicked.connect(self.choose_data_file)

        self.sample_label = QLabel(self.data_tab.group_box_detection)
        self.sample_label.setText("# Samples: ")
        self.sample_label.resize(300, 20)
        self.sample_label.move(200, 80)

        self.num_samples = QLineEdit(self.data_tab.group_box_detection)
        self.num_samples.resize(100, 20)
        self.num_samples.move(275, 80)


        self.search_button = QPushButton(self.data_tab.group_box_detection)
        self.search_button.move(685, 120)
        self.search_button.resize(100, 25)
        self.search_button.setEnabled(False)
        self.search_button.setText("Search")
        self.search_button.clicked.connect(self.search)

        self.speed_test_button = QPushButton(self.data_tab.group_box_detection)
        self.speed_test_button.move(685, 160)
        self.speed_test_button.resize(100, 25)
        self.speed_test_button.setEnabled(False)
        self.speed_test_button.setText("Speed Test")
        self.speed_test_button.clicked.connect(self.speed_test)

        # self.memory_test_button = QPushButton(self.data_tab.group_box_detection)
        # self.memory_test_button.move(685, 160)
        # self.memory_test_button.setEnabled(False)
        # self.memory_test_button.resize(100, 25)
        # self.memory_test_button.setText("Memory Test")
        # self.memory_test_button.clicked.connect(self.memory_test)

        self.load_test_data = QPushButton(self.data_tab.group_box_detection)
        self.load_test_data.move(410, 90)
        self.load_test_data.resize(120, 30)
        self.load_test_data.setText("Load Test Data")
        self.load_test_data.clicked.connect(self.load_sample_test_data)


        self.column_label = QLabel(self.data_tab.group_box_detection)
        self.column_label.setText("Column #: ")
        self.column_label.resize(100, 20)
        self.column_label.move(207, 110)

        self.column_text = QLineEdit(self.data_tab.group_box_detection)
        self.column_text.resize(100, 20)
        self.column_text.move(275, 110)


        self.generate_data = QPushButton(self.data_tab.group_box_detection)
        self.generate_data.move(410, 160)
        self.generate_data.setText("Generate Random Data")
        self.generate_data.resize(175, 20)
        self.generate_data.clicked.connect(self.generate_random_data)

        self.random_data_size_label = QLabel(self.data_tab.group_box_detection)
        self.random_data_size_label.setText("Size: ")
        self.random_data_size_label.resize(100, 20)
        self.random_data_size_label.move(233, 160)

        self.random_data_size = QLineEdit(self.data_tab.group_box_detection)
        self.random_data_size.resize(100, 20)
        self.random_data_size.move(275, 160)

        self.search_enable(False)
        self.test_enable(False)
        verticalSpacer2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        detection_box.addItem(verticalSpacer2)

        ############### Console Box ############################################
        console_box = QVBoxLayout()
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.move(590, 30)
        self.console.resize(50,50)
        self.console.setText("> ")
        console_box.addWidget(self.console)


        self.consoleCursor = self.console.textCursor()
        self.data_tab.group_box_database.setLayout(database_box)
        self.data_tab.group_box_detection.setLayout(detection_box)
        self.data_tab.group_box_console.setLayout(console_box)

        self.data_tab.setStyleSheet("""

            QGroupBox {
                border: 1px solid gray;
                border-radius: 9px;
                margin-top: 0.5em;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }

            QTextEdit {
                font-family: Menlo, Consolas, Monaco, Lucida Console;
            }

            QLabel {
                font: 9pt Consolas;
            }
            QCheckBox {
                width: 30px;
                font: 12pt Consolas;
                color: #98FB98;
                margin-left 30px;
            }

            QLineEdit {
                font: 8pt Consolas;
                color: rgb(255, 0, 0);
            }


        """)

        ########################################################################

        ############################################
        #                                          #
        #                 GPU Tab                  #
        #                                          #
        ############################################
        self.gpu_tab.data_textbox = QTextEdit(self.gpu_tab)
        self.gpu_tab.data_textbox.setReadOnly(True)
        self.gpu_tab.data_textbox.move(190, 30)
        self.gpu_tab.data_textbox.resize(600,600)
        self.gpu_tab.data_textbox.setText(devices.get_info(0))

        self.gpu_tab.label = QLabel(self.gpu_tab)
        self.gpu_tab.label.move(50, 25)
        self.gpu_tab.label.resize(60, 40)
        self.gpu_tab.label.setText("Device:")

        self.gpu_tab.combobox = QComboBox(self.gpu_tab)
        self.gpu_tab.combobox.setGeometry(QRect(110, 30, 50, 31))
        self.gpu_tab.combobox.setObjectName(("Device Number"))
        self.gpu_tab.combobox.currentTextChanged.connect(self.on_combo_changed)
        for i in range(devices.num_devices):
            self.gpu_tab.combobox.addItem(str(i))
        ########################################################################

        ############################################
        #                                          #
        #               About Tab                  #
        #                                          #
        ############################################

        ########################################################################

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
            self.console_append("Finished adding data", True)
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
    database = access.Connection("localhost", "root", "", "domains", False)
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


# readPath = directoryPath + '/Data/DomainData.csv' # path to our raw and unprocessed data
#
# chunksize = 1000000

# process.process_and_insert_data(readPath, chunksize, database, 'Connection')


"""
readpath = '/home/trevor/Documents/MaliciousDomainDetection/Data/localdomaindata.csv'


matcher = matcher.Matcher(readpath)


matcher.time_diff(30)

while(True):
    print("Enter a domain to be checked: ", end='')
    word = input()
    start_time1 = time.time()
    isMal1 = matcher.is_malicious_cpu(word)
    end_time1 = time.time() - start_time1

    start_time2 = time.time()
    isMal2 = matcher.is_malicious(word)
    end_time2 = time.time() - start_time2

    if (isMal1 and isMal2):
        print("Result: Malicious | GPU Time: " + str(end_time2) + " | CPU Time: " + str(end_time1))
    else:
        print("Result: Safe | GPU Time: " + str(end_time2) + " | CPU Time: " + str(end_time1))

"""
