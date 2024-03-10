import time

from gantry_movement import IMarlinClient

class MockMarlinClient(IMarlinClient):
    def home(self):
        print("MockMarlinClient: homing")
        time.sleep(1)

    def set_speed(self, speed):
        print(f"MockMarlinClient: setting speed to {speed}")
        time.sleep(1)

    def move_to_position(self, x, z):
        print(f"MockMarlinClient: moving to ({x}, {z})")
        time.sleep(1)
