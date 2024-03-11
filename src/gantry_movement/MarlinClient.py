import serial
import time

from .IMarlinClient import IMarlinClient
from .utils import poll_for_ok

class MarlinClient(IMarlinClient):

    serial_port: serial.Serial

    def __init__(self, com_port, baud_rate):

        try:
            self.serial_port = serial.Serial(port=com_port, baudrate=baud_rate, timeout=1)
        except serial.SerialException:
            raise ValueError("Failed to connect to Marlin, check the serial port")
        
    def home(self):
        self.serial_port.reset_input_buffer()
        self.serial_port.write(b"G28 X\r\n")
        poll_for_ok(self.serial_port)
        self.serial_port.write(b"G28 Z\r\n")
        poll_for_ok(self.serial_port)

    def set_speed(self, speed):
        pass

    def move_to_position(self, x, z):
        self.serial_port.reset_input_buffer()
        self.serial_port.write(f"G1 X{x} Z{z}\r\n".encode(encoding="utf_8"))
        poll_for_ok(self.serial_port)
        self.serial_port.write("M400")
        poll_for_ok(self.serial_port)
