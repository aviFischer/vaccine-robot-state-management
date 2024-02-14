from transitions import Machine

from .IVaccineRobot import IVaccineRobot
from gantry_movement import IMarlinClient
from raspberrypi_gpio import IGpioClient

class VaccineRobot(IVaccineRobot):

    states = ["idle", "determine_injection_location", "vaccine_retrieval", "vaccine_delivery", "vaccine_disposal", "error"]
    state_machine: Machine

    marlin_client: IMarlinClient
    gpio_client: IGpioClient

    injection_location: (float, float)

    def __init__(self, marlin_client: IMarlinClient, gpio_client: IGpioClient):
        self.state_machine = Machine(model=self, states=self.states, initial="idle")

        # setting up transition logic
        self.state_machine.add_transition(trigger="injection_started", source="idle", dest="determine_injection_location")
        self.state_machine.add_transition(trigger="shoulder_detected", source="determine_injection_location", dest="vaccine_retrieval")
        self.state_machine.add_transition(trigger="shoulder_detection_failed", source="determine_injection_location", dest="error")
        self.state_machine.add_transition(trigger="vaccine_picked_up", source="vaccine_retrieval", dest="vaccine_delivery")
        self.state_machine.add_transition(trigger="vaccine_pickup_failed", source="vaccine_retrieval", dest="error")
        self.state_machine.add_transition(trigger="vaccine_delivered", source="vaccine_delivery", dest="vaccine_disposal")
        #TODO finish this

        # wiring side effects to states
        self.state_machine.on_enter_vaccine_retrieval("vaccine_pickup")
        # TODO finish this


        self.marlin_client = marlin_client
        self.gpio_client = gpio_client

    def set_injection_location(self, location):
        self.injection_location = location
        print(f"New injection location: {location}")

    def get_current_state(self):
        return self.state_machine.get_state()

    # side effect functions
    def vaccine_pickup():
        pass

    # "Event" functions
    def injection_started(self):
        pass

    def shoulder_detected(self):
        pass

    def shoulder_detection_failed(self):
        pass

    def vaccine_picked_up(self):
        pass

    def vaccine_pickup_failed(self):
        pass

    def vaccine_delivered(self):
        pass

    def vaccine_delivery_failed(self):
        pass

    def vaccine_disposed(self):
        pass

    def vaccine_disposal_failed(self):
        pass

    def error_cleared(self):
        pass
