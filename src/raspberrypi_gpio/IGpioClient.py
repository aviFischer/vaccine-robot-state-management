from abc import ABC, abstractmethod

class IGpioClient(ABC):

    @abstractmethod
    def get_breakbeam_sensor(self) -> int:
        pass

    @abstractmethod
    def engage_disposal_mechanism(self):
        pass

    @abstractmethod
    def retract_disposal_mechanism(self):
        pass

    @abstractmethod
    def engage_plunger(self):
        pass

    @abstractmethod
    def retract_plunger(self):
        pass
