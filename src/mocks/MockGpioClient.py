import time

from raspberrypi_gpio import IGpioClient

class MockGpioClient(IGpioClient):

    def get_breakbeam_sensor() -> int:
        print("MockGpioClient: Getting sensor reading")
        return 1

    def engage_disposal_mechanism():
        print("MockGpioClient: Engaging disposal mechanism")
        time.sleep(1)

    def retract_disposal_mechanism():
        print("MockGpioClient: Retracting disposal mechanism")
        time.sleep(1)

    def engage_plunger():
        print("MockGpioClient: Engaging Plunger")
        time.sleep(1)

    def retract_plunger():
        print("MockGpioClient: Retracting Plunger")
        time.sleep(1)
