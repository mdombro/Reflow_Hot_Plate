import sys
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import serial

class TempControl(QMainWindow):
    def __init__(self, processMessages, pidMessages):
        #super(TempControl, self).__init__(parent)
        super().__init__()
        self.title = 'Temperature Control GUI'
        self.processMessages = processMessages
        self.pidMessages = pidMessages
        self.startGUI()

    def startGUI(self):
        self.setWindowTitle(self.title)
        self.layout = QGridLayout(self)
        self.leftMenus = QVBoxLayout()
        self.layout.addLayout(self.leftMenus, 1, 1)
        self.portComboBox = QComboBox(self)
        print(self.processMessages)
        while len(self.processMessages['serial']['portList']) == 0:
            pass
        ports = self.processMessages['serial']['portList']
        for i in ports:
            self.portComboBox.addItem(i)
        self.leftMenus.addWidget(self.comboBox)

        self.setLayout(self.layout)


