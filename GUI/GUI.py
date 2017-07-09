import sys
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import serial

class TempControl(QWidget):
    def __init__(self, processMessagePipe, pidMessagePipe):
        super().__init__()
        self.title = 'Temperature Control GUI'
        self.processMessages = processMessagePipe
        self.pidMessages = pidMessagePipe
        self.startGUI()

    def startGUI(self):
        self.setWindowTitle(self.title)
        self.setMinimumSize(1400, 800)
        self.layout = QGridLayout()
        self.layout.setSpacing(5)
        #self.layout.setColumnStretch(0,4)
        #self.layout.setRowStretch(0,4)
        self.setLayout(self.layout)
        self.menus = QVBoxLayout()
        self.layout.addLayout(self.menus, 0, 0)

        self.portComboBox = QComboBox(self)
        ports = self.processMessages.recv()
        for i in ports['data']:
            self.portComboBox.addItem(i)
        self.menus.addWidget(self.portComboBox)

        self.connectButton = QPushButton('Connect')
        self.connectButton.clicked.connect(self.connectuC)
        self.menus.addWidget(self.connectButton)
        #self.connectionStatus = QLabel('')
        #self.layout.addWidget(self.connectionStatus, 1, 0)

        #self.menus.addSpacing(100)
        spacer = QSpacerItem(10, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.menus.addItem(spacer)

        self.currentTempInd = QLabel('Current Temp: ')
        self.currentTemp = QLabel('0.00')
        self.menus.addWidget(self.currentTempInd)
        self.menus.addWidget(self.currentTemp)

        self.setPointInd = QLabel('Setpoint Temperature: ')
        self.setPoint = QLabel('0.00')
        self.menus.addWidget(self.setPointInd)
        self.menus.addWidget(self.setPoint)

        spacer = QSpacerItem(10, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.menus.addItem(spacer)
        self.menus.addStretch()



    def connectuC(self):
        self.port = self.portComboBox.currentText()
        self.processMessages.send({'type': 'portSelected',
                                  'data': self.port})
        success = self.processMessages.recv()
        # if success['data'] == 'connectionError':
        #     self.connectionStatus.setText('Error Connecting!')
        # else:
        #     self.connectionStatus.setText('Connected!')



