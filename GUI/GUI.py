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
        self.layout = QGridLayout()
        self.layout.setSpacing(5)
        self.layout.setColumnStretch(0,4)
        self.layout.setRowStretch(0,4)
        self.setLayout(self.layout)


        self.portComboBox = QComboBox(self)
        ports = self.processMessages.recv()
        for i in ports['data']:
            self.portComboBox.addItem(i)
        self.layout.addWidget(self.portComboBox, 0, 0)

        self.connectButton = QPushButton('Connect')
        self.connectButton.clicked.connect(self.connectuC)
        self.layout.addWidget(self.connectButton, 0, 1)
        self.connectionStatus = QLabel('')
        self.layout.addWidget(self.connectionStatus, 1, 0)

    def connectuC(self):
        self.port = self.portComboBox.currentText()
        self.processMessages.send({'type': 'portSelected',
                                  'data': self.port})
        success = self.processMessages.recv()
        if success['data'] == 'connectionError':
            self.connectionStatus.setText('Error Connecting!')
        else:
            self.connectionStatus.setText('Connected!')



