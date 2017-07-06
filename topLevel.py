from GUI.GUI import TempControl
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import *
from multiprocessing import Queue, Process
from Common.SerialHandler import SerialHandler
from Common.PID import PID
import sys

def main():
    # Q U E U E s
        # SerialHandler puts, PID gets, PID then uses data to compute PID output
    uC_to_pc = Queue()
    uC_to_pc.cancel_join_thread()
        # PID puts, SerialHandler gets, and then sends to uC
    pc_to_uC = Queue()
    pc_to_uC.cancel_join_thread()

    # P R O C E S S E S
    SerialComm = SerialHandler()
    PIDobj = PID()

    SerialCommProc = Process(target=SerialComm.run(), args=(uC_to_pc, pc_to_uC))
    PIDProc = Process(target=PIDobj.run(), args=(uC_to_pc, pc_to_uC))
    SerialCommProc.start()
    PIDProc.start()

    app = QApplication(sys.argv)
    window = TempControl()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

