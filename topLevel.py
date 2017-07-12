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
    # Q U E U E s
        # SerialHandler puts, PID gets, PID then uses data to compute PID output
    uC_to_pc = Queue()
    uC_to_pc.cancel_join_thread()
        # PID puts, SerialHandler gets, and then sends to uC
    pc_to_uC = Queue()
    pc_to_uC.cancel_join_thread()
    serial_to_GUI_serial_side, serial_to_GUI_GUI_side = Pipe()
    serial_to_PID_serial_side, serial_to_PID_PID_side = Pipe()
    PID_to_serial_PID_side, PID_to_serial_serial_side = Pipe()
    GUI_to_PID_GUI_side, GUI_to_PID_PID_side = Pipe()
    # serialMessageParent, serialMessageChild = Pipe()
    # pidMessagePipe = Pipe()

    # M A N A G E R
    # holds shared state dictionaries to be accesed by processes
    # ToDo: will replace the Pipes()
    manager = Manager()
    processMessages = manager.dict()
    processMessages.update({'serial': {}})
    processMessages['serial'] = {'portList': [],
                                 'portSelected': '',
                                 'connFail': False,
                                 'connectionError': False}



    # P R O C E S S E S
    SHUTDOWN = Event()
    processes = []
    SerialCommProc = Process(target=runSerial, args=(serial_to_GUI_serial_side, serial_to_PID_serial_side, PID_to_serial_serial_side, SHUTDOWN))
    PIDProc = Process(target=runPID, args=(PID_to_serial_PID_side, GUI_to_PID_PID_side, SHUTDOWN))
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

