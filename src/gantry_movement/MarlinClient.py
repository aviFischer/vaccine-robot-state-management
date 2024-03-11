import serial

from .IMarlinClient import IMarlinClient

class MarlinClient(IMarlinClient):

    def __init__(self, com_port, baud_rate):

        try:
            self.serial_port = serial.Serial(port=com_port, baudrate=baud_rate, timeout=1)
        except serial.SerialException:
            raise ValueError("Failed to connect to Marlin, check the serial port")

    def home(self):
        self.serial_port.write(b"G28 X")
        self.serial_port.read(size=2)
        self.serial_port.write(b"G28 Z")
        self.serial_port.read(size=2)

    def set_speed(self, speed):
        pass

    def move_to_position(self, x, z):
        self.serial_port.write(f"G1 X{x} Z{z}".encode(encoding="utf_8"))
