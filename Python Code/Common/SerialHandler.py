import serial
import sys
import glob
import time

class SerialHandler:
    def __init__(self, serial_to_GUI_serial_side, serial_to_PID_serial_side, PID_to_serial_serial_side, shutdown):
        self.ser = ''
        self.to_gui_messages = serial_to_GUI_serial_side
        self.to_pid_messages = serial_to_PID_serial_side
        self.from_pid_messages = PID_to_serial_serial_side
        self.shutdown = shutdown

    def readLine(self):
        return self.serObj.readline()

    def init(self):
        ports = self.serial_ports()
        print(ports)
        self.to_gui_messages.send({'type': 'portList',
                                      'data': ports})
        portM = self.to_gui_messages.recv()
        port = portM['data']
        print(port)
        try:
            self.connect(port)
        except serial.serialutil.SerialException:
            self.to_gui_messages.send({'type': 'connectionStatus',
                                          'data': 'connectionError'})
            self.init()
        else:
            self.to_gui_messages.send({'type': 'connectionStatus',
                                          'data': 'connected'})
            self.serObj.write(b'Hello')
            time.sleep(0.2)
            self.run()

    def connect(self, port):
        self.port = port
        self.serObj = serial.Serial(port, 9600, timeout=1.0)

    def run(self):
        while not self.shutdown.is_set():
            data = self.readLine()
            print(data)
            data = data[0:2]
            dataPacket = {'type': 'tempReading',
                          'data': data}
            self.to_pid_messages.send(dataPacket)
            self.to_gui_messages.send(dataPacket)
            # TODO: uncomment these lines
            #dutyCycle = self.from_pid_messages.recv()
            #self.serObj.write(b'H' + dutyCycle)

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

def runSerial(serial_to_GUI_serial_side, serial_to_PID_serial_side, PID_to_serial_serial_side, SHUTDOWN):
    serObj = SerialHandler(serial_to_GUI_serial_side, serial_to_PID_serial_side, PID_to_serial_serial_side, SHUTDOWN)
    serObj.init()


