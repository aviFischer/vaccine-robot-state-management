from abc import ABC, abstractmethod

class IVaccineRobot(ABC):

    # event functions
    @abstractmethod
    def send_injection_started(self):
        pass

    @abstractmethod
    def send_shoulder_detected(self):
        pass

    @abstractmethod
    def send_shoulder_detection_failed(self):
        pass

    @abstractmethod
    def send_vaccine_picked_up(self):
        pass

    @abstractmethod
    def send_vaccine_pickup_failed(self):
        pass

    @abstractmethod
    def send_vaccine_delivered(self):
        pass

    @abstractmethod
    def send_vaccine_delivery_failed(self):
        pass

    @abstractmethod
    def send_vaccine_disposed(self):
        pass

    @abstractmethod
    def send_vaccine_disposal_failed(self):
        pass

    @abstractmethod
    def send_error_cleared(self):
        pass

    # side effect functions
    @abstractmethod
    def determine_injection_location(self):
        pass

    @abstractmethod
    def vaccine_pickup(self):
        pass

    @abstractmethod
    def vaccine_delivery(self):
        pass

    @abstractmethod
    def vaccine_disposal(self):
        pass

    # Getters and setters
    @abstractmethod
    def set_injection_location(self, location):
        pass

    @abstractmethod
    def get_current_state(self):
        pass

    @abstractmethod
    def move_to_shoulder(self):
        pass
