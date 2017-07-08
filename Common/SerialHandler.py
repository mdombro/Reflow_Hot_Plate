import serial

class SerialHandler:
    def __init__(self, uC_to_pc, pc_to_uC, portname, shutdown):
        self.ser = ''
        self.portname = portname
        self.shutdown = shutdown
        self.uC_to_pc = uC_to_pc
        self.pc_to_uC = pc_to_uC
        self.ser = serial.Serial(self.portname, 9600, timeout=1.0)

    def readLine(self):
        return self.ser.readline()

    def run(self):
        while not self.shutodown.is_set():
            data = self.readLine()
            self.uC_to_pc.put(data)
            dutyCycle = self.pc_to_uC.get()
            self.write(b'H' + dutyCycle)

def runSerial(uC_to_pc, pc_to_uC, shutodown):
    portName = 'COM3'
    try:
        print('Trying to open port %s' % portName)
        serObj = SerialHandler(uC_to_pc, pc_to_uC, portName, shutodown)
        serObj.run()
    except serial.serialutil.SerialException:
        print('Could not open port.. Check connections')
        shutodown.set()
