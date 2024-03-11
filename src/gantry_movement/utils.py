import serial

def poll_for_ok(serial_port: serial.Serial):
    last_line = ""
    while(last_line != b"ok"):
        last_line = serial_port.readline()
        print(f"Serial Message: {last_line}")
