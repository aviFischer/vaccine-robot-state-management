from abc import ABC, abstractmethod

class IVaccineRobot(ABC):

    # "Event" functions
    @abstractmethod
    def injection_started(self):
        pass

    @abstractmethod
    def shoulder_detected(self, location):
        pass

    @abstractmethod
    def shoulder_detection_failed(self):
        pass

    @abstractmethod
    def vaccine_picked_up(self):
        pass

    @abstractmethod
    def vaccine_pickup_failed(self):
        pass

    @abstractmethod
    def vaccine_delivered(self):
        pass

    @abstractmethod
    def vaccine_delivery_failed(self):
        pass

    @abstractmethod
    def vaccine_disposed(self):
        pass

    @abstractmethod
    def vaccine_disposal_failed(self):
        pass

    @abstractmethod
    def error_cleared(self):
        pass

    # Getters and setters
    @abstractmethod
    def set_injection_location(self, location):
        pass

    @abstractmethod
    def get_current_state(self):
        pass
