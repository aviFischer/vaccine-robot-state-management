import time

from raspberrypi_gpio import IGpioClient

class MockGpioClient(IGpioClient):

    def get_breakbeam_sensor() -> int:
        time.sleep(0.1)
        return 1

    def engage_disposal_mechanism():
        time.sleep(1)

    def retract_disposal_mechanism():
        time.sleep(1)
