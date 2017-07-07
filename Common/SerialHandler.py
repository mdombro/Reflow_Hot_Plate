import serial

class SerialHandler:
    def __init__(self):
        self.ser = serial.Serial('COM3', 9600, timeout=1.0)
    def readLine(self):
        return self.ser.readline()


def runSerial(uC_to_pc, pc_to_uC):
    serObj = SerialHandler()
    while True:
        data = serObj.readLine()
        uC_to_pc.put(data)
        dutyCycle = pc_to_uC.get()
        serObj.write(b'H' + dutyCycle)