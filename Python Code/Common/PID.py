class PID:
    def __init__(self):
        pass

def runPID(PID_to_serial_PID_side, serial_to_PID_PID_side, GUI_to_PID_PID_side, SHUTDOWN):
    while not SHUTDOWN.is_set():
        a = serial_to_PID_PID_side.recv()
    #pass #print("testing PID")
    print(SHUTDOWN.is_set(), "At PID level")