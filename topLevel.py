from GUI.GUI import TempControl
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import *
from multiprocessing import Queue, Process
from Common.SerialHandler import SerialHandler
from Common.PID import PID
import sys

def main():
    # Q U E U E s
    uC_to_pc = Queue()
    uC_to_pc.cancel_join_thread()
    pc_to_uC = Queue()
    pc_to_uC.cancel_join_thread()

    # P R O C E S S E S
    SerialComm = SerialHandler()
    PIDobj = PID()

    SerialCommProc = Process(target=SerialComm.run(), args=())
    PIDProc = Process(target=PIDobj.run(), args=())



    app = QApplication(sys.argv)
    window = TempControl()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

