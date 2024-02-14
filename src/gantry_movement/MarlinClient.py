import serial

from .IMarlinClient import IMarlinClient

class MarlinClient(IMarlinClient):

    serial_port: serial.Serial

    def __init__(self, com_port, baud_rate):

        try:
            self.serial_port = serial.Serial(port=com_port, baudrate=baud_rate, timeout=1)
        except serial.SerialException:
            raise ValueError("Failed to connect to Marlin, check the serial port")

    def home(self):
        self.serial_port.write('G28 X Z')
        self.serial_port.read(size=2)

    def set_speed(self, speed):
        pass

    def move_to_position(self, x, z):
        pass