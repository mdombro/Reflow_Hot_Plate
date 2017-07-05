import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class TempControl(QWidget):
    def __init__(self):
        #super(TempControl, self).__init__(parent)
        super().__init__()
        self.title = 'Temperature Control GUI'
        self.name = QLabel('Name: ')
        self.startGUI()

    def startGUI(self):
        self.setWindowTitle(self.title)