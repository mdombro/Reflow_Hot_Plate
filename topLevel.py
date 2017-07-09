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
    serialMessagePipe = Pipe()
    pidMessagePipe = Pipe()

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
    print('Top level')
    print(processMessages)



    # P R O C E S S E S
    SHUTDOWN = Event()
    processes = []
    SerialCommProc = Process(target=runSerial, args=(uC_to_pc, pc_to_uC, processMessages, SHUTDOWN))
    PIDProc = Process(target=runPID, args=(uC_to_pc, pc_to_uC, processMessages, SHUTDOWN))
    processes.append((SerialCommProc, SHUTDOWN))
    processes.append((PIDProc, SHUTDOWN))

    # G U I
    app = QApplication(sys.argv)
    window = TempControl(serialMessagePipe, pidMessagePipe)
    window.show()

    SerialCommProc.start()
    PIDProc.start()
    app.exec_()

    for _, S in processes:
        S.set()
    for p, _ in processes:
        p.join()

if __name__ == '__main__':
    main()

