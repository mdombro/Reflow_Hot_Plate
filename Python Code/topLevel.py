from GUI.GUI import TempControl
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import *
from multiprocessing import Queue, Process, Event, Pipe, Manager
from Common.SerialHandler import runSerial
from Common.PID import runPID
import sys
import glob
import serial

def main():
    # P I P E S
        # PID puts, SerialHandler gets, and then sends to uC
    serial_to_GUI_serial_side, serial_to_GUI_GUI_side = Pipe()
    serial_to_PID_serial_side, serial_to_PID_PID_side = Pipe()
    PID_to_serial_PID_side, PID_to_serial_serial_side = Pipe()
    GUI_to_PID_GUI_side, GUI_to_PID_PID_side = Pipe()

    # P R O C E S S E S
    SHUTDOWN = Event()
    processes = []
    SerialCommProc = Process(target=runSerial, args=(serial_to_GUI_serial_side, serial_to_PID_serial_side, PID_to_serial_serial_side, SHUTDOWN))
    PIDProc = Process(target=runPID, args=(PID_to_serial_PID_side, serial_to_PID_PID_side, GUI_to_PID_PID_side, SHUTDOWN))
    processes.append((SerialCommProc, SHUTDOWN))
    processes.append((PIDProc, SHUTDOWN))
    SerialCommProc.start()
    PIDProc.start()

    # G U I
    app = QApplication(sys.argv)
    window = TempControl(GUI_to_PID_GUI_side, serial_to_GUI_GUI_side)
    window.show()

    app.exec_()
    SHUTDOWN.set()

    for _, S in processes:
        S.set()
    for p, _ in processes:
        p.join()

if __name__ == '__main__':
    main()

