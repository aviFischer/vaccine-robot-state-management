from abc import ABC, abstractmethod

class IGpioClient(ABC):

    @abstractmethod
    def get_breakbeam_sensor() -> int:
        pass

    @abstractmethod
    def engage_disposal_mechanism():
        pass

    @abstractmethod
    def retract_disposal_mechanism():
        pass
