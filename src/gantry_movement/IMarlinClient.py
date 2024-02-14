from abc import ABC, abstractmethod

class IMarlinClient(ABC):

    @abstractmethod
    def home(self):
        pass

    @abstractmethod
    def set_speed(self, speed):
        pass

    @abstractmethod
    def move_to_position(self, x, z):
        pass
