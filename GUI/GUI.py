import sys
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import serial
import pyqtgraph as pg
import numpy as np

class TempControl(QWidget):
    def __init__(self, processMessagePipe, pidMessagePipe):
        super().__init__()
        self.title = 'Temperature Control GUI'
        self.processMessages = processMessagePipe
        self.pidMessages = pidMessagePipe
        self.infoFontSize = 20
        self.buttonFontSize = 14
        self.startStopFontSize = 24
        self.startGUI()

    def startGUI(self):
        ########################################
        #                                      #
        #              Setup                   #
        #                                      #
        ########################################
        self.setWindowTitle(self.title)
        self.setMinimumSize(1400, 800)
        self.layout = QGridLayout()
        self.layout.setSpacing(5)
        #self.layout.setColumnStretch(0,4)
        #self.layout.setRowStretch(0,4)
        self.setLayout(self.layout)
        self.menus = QVBoxLayout()
        self.layout.addLayout(self.menus, 0, 0)
        pg.setConfigOptions(antialias=True)
        self.pwin = pg.GraphicsWindow()
        self.layout.addWidget(self.pwin, 0, 1, 1, 6)

        ########################################
        #                                      #
        #       Buttons and feedback           #
        #                                      #
        ########################################
        self.portComboBox = QComboBox(self)
        self.portComboBox.setFont(QtGui.QFont("Times", self.buttonFontSize, QtGui.QFont.Bold))
        ports = self.processMessages.recv()
        for i in ports['data']:
            self.portComboBox.addItem(i)
        self.menus.addWidget(self.portComboBox)

        self.connectButton = QPushButton('Connect')
        self.connectButton.clicked.connect(self.connectuC)
        self.connectButton.setFont(QtGui.QFont("Times", self.infoFontSize, QtGui.QFont.Bold))
        self.menus.addWidget(self.connectButton)
        #self.connectionStatus = QLabel('')
        #self.layout.addWidget(self.connectionStatus, 1, 0)

        #self.menus.addSpacing(100)
        spacer = QSpacerItem(10, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.menus.addItem(spacer)

        self.currentTempInd = QLabel('Current Temp')
        self.currentTempInd.setFont(QtGui.QFont("Times", self.infoFontSize, QtGui.QFont.Bold))
        self.currentTemp = QLabel('0.00')
        self.currentTemp.setFont(QtGui.QFont("Times", self.infoFontSize, QtGui.QFont.Bold))
        self.menus.addWidget(self.currentTempInd)
        self.menus.addWidget(self.currentTemp)
        spacer = QSpacerItem(10,40,QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.menus.addItem(spacer)
        self.setPointInd = QLabel('Setpoint Temperature')
        self.setPointInd.setFont(QtGui.QFont("Times", self.infoFontSize, QtGui.QFont.Bold))
        self.setPoint = QLabel('0.00')
        self.setPoint.setFont(QtGui.QFont("Times", self.infoFontSize, QtGui.QFont.Bold))
        self.menus.addWidget(self.setPointInd)
        self.menus.addWidget(self.setPoint)

        spacer = QSpacerItem(10, 70, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.menus.addItem(spacer)

        self.go = QPushButton("GO")
        self.go.setFont(QtGui.QFont("Times", self.startStopFontSize, QtGui.QFont.Bold))
        self.stop = QPushButton("STOP")
        self.stop.setFont(QtGui.QFont("Times", self.startStopFontSize, QtGui.QFont.Bold))
        # Todo: connect these to serial functions
        self.menus.addWidget(self.go)
        self.menus.addWidget(self.stop)

        spacer = QSpacerItem(10, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.menus.addItem(spacer)
        self.menus.addStretch()

        ########################################
        #                                      #
        #              Plotting                #
        #                                      #
        ########################################
        self.plot = self.pwin.addPlot(title='Basic Test', y = np.random.normal(size=100))


    def connectuC(self):
        self.port = self.portComboBox.currentText()
        self.processMessages.send({'type': 'portSelected',
                                  'data': self.port})
        success = self.processMessages.recv()
        # if success['data'] == 'connectionError':
        #     self.connectionStatus.setText('Error Connecting!')
        # else:
        #     self.connectionStatus.setText('Connected!')



