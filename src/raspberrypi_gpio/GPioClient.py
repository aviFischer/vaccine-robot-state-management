from .IGpioClient import IGpioClient

class GpioClient(IGpioClient):

    def get_breakbeam_sensor() -> int:
        return 0

    def engage_disposal_mechanism():
        pass

    def retract_disposal_mechanism():
        pass
