from GUI.GUI import TempControl
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import *
import sys

def main():
    app = QApplication(sys.argv)
    window = TempControl()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

