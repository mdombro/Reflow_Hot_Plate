import serial
import sys
import glob
from multiprocessing import Manager

class SerialHandler:
    def __init__(self, uC_to_pc, pc_to_uC, processMessages, shutdown):
        self.ser = ''
        self.processMessages = processMessages
        self.shutdown = shutdown
        self.uC_to_pc = uC_to_pc
        self.pc_to_uC = pc_to_uC
        #self.ser = serial.Serial(self.portname, 9600, timeout=1.0)

    def readLine(self):
        return self.serObj.readline()

    def init(self):
        ports = self.serial_ports()
        self.processMessages['serial']['portList'] = ports
        while self.processMessages['serial']['portSelected'] == '':
            pass
        port = self.processMessages['serial']['portSelected']
        try:
            self.connect(port)
        except serial.serialutil.SerialException:
            self.processMessages['serial']['connectionError'] = True
            self.init()
        else:
            self.run()

    def connect(self, port):
        self.port = port
        self.serObj = serial.Serial(port, 9600, timeout=1.0)

    def run(self):
        while not self.shutdown.is_set():
            data = self.readLine()
            self.uC_to_pc.put(data)
            dutyCycle = self.pc_to_uC.get()
            self.serObj.write(b'H' + dutyCycle)

    # https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
    # finds existing ports on the system
    def serial_ports(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

def runSerial(uC_to_pc, pc_to_uC, processMessages, shutdown):
    print('called function')
    print(processMessages)
    serObj = SerialHandler(uC_to_pc, pc_to_uC, processMessages, shutdown)
    serObj.init()


