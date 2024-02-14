import time

from gantry_movement import IMarlinClient

class MockMarlinClient(IMarlinClient):
    def home(self):
        time.sleep(1)

    def set_speed(self, speed):
        time.sleep(1)

    def move_to_position(self, x, z):
        time.sleep(1)
