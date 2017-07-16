import sys
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import serial
import pyqtgraph as pg
import numpy as np
import threading

class TempControl(QMainWindow):
    signalNewTemp = pyqtSignal(float)
    def __init__(self, GUI_to_PID_GUI_side, serial_to_GUI_GUI_side):
        super().__init__()
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.title = 'Temperature Control GUI'
        self.ThermalCurvePidMessages = GUI_to_PID_GUI_side
        self.serialMessages = serial_to_GUI_GUI_side
        self.infoFontSize = 20
        self.buttonFontSize = 14
        self.startStopFontSize = 24
        self.accum = []
        self.signalNewTemp.connect(self.updatePlot)
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
        self.centralWidget.setLayout(self.layout)
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
        ports = self.serialMessages.recv()
        if ports['type'] == 'portList':
            for i in ports['data']:
                self.portComboBox.addItem(i)
        self.menus.addWidget(self.portComboBox)

        self.connectButton = QPushButton('Connect')
        self.connectButton.clicked.connect(self.connectuC)
        self.connectButton.setFont(QtGui.QFont("Times", self.infoFontSize, QtGui.QFont.Bold))
        self.menus.addWidget(self.connectButton)
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusLabel = QLabel('')
        self.statusBar.addWidget(self.statusLabel)
        self.connectionStatus = QLabel('')
        self.layout.addWidget(self.connectionStatus, 1, 0)

        #self.menus.addSpacing(100)
        spacer = QSpacerItem(10, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.menus.addItem(spacer)

        self.currentTempInd = QLabel('Current Temp °C:')
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
        #self.p1temp = self.pwin.addPlot(title='Basic Test', y = np.random.normal(size=100))
        self.p1temp = self.pwin.addPlot(title='<font size="100">Plate Temperature and Thermal Profile</font>', labels={'left':'<font size="100"> Temperature °C</font>', 'bottom':'<font size="100">Time</font>'})
        self.p1temp.setYRange(0, 250)
        self.p1temp.setMouseEnabled(x=False, y=False)
        self.p1 = self.p1temp.plot(pen='y')


    def updatePlot(self, temp):
        self.accum.append(temp)
        self.p1.setData(self.accum, pen='y')
        self.currentTemp.setText(str(temp))

    def connectuC(self):
        self.port = self.portComboBox.currentText()
        self.serialMessages.send({'type': 'portSelected',
                                  'data': self.port})
        success = self.serialMessages.recv()
        if success['type'] == 'connectionStatus' and success['data'] == 'connectionError':
            self.statusLabel.setText('Error Connecting!')
            print('Error Connecting!')
        else:
            self.statusLabel.setText('Connected!')
            print('Connected!')
            threading.Thread(target=serialWatcher, name='serialWatcher', args=(self.signalNewTemp, self.serialMessages)).start()


def serialWatcher(signalNewTemp, serialMessages):
    temp = 0
    tempLast = temp
    while True:
        t = serialMessages.recv()
        print(t)
        if t['type'] == 'tempReading':
            temp = int.from_bytes(t['data'][0:2], byteorder='big')
            temp = temp>>2
            temp *= 0.25
            tempLast = temp
            signalNewTemp.emit(temp)
        else:
            temp = tempLast
        # Todo: check for a fault message, set status bar to Fault!, maybe try and keep track/hold temp to keep PID running
        # while below some timeout condition, then send everything a shutdown (µC especially)
        print('Read temp: ', temp)


