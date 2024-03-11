from transitions import Machine

from .IVaccineRobot import IVaccineRobot
from gantry_movement import IMarlinClient
from raspberrypi_gpio import IGpioClient
from .utils import verify_shoulder_location, webcam_to_gantry

class VaccineRobot(IVaccineRobot):

    states = ["idle", "determine_injection_location", "vaccine_retrieval", "vaccine_delivery", "vaccine_disposal", "error"]
    state_machine: Machine

    marlin_client: IMarlinClient
    gpio_client: IGpioClient

    injection_location: tuple[float, float]

    def __init__(self, marlin_client: IMarlinClient, gpio_client: IGpioClient):
        self.state_machine = Machine(model=self, states=self.states, initial="idle")

        # setting up transition logic
        self.state_machine.add_transition(trigger="injection_started", source="idle", dest="determine_injection_location")
        self.state_machine.add_transition(trigger="shoulder_detected", source="determine_injection_location", dest="vaccine_retrieval")
        self.state_machine.add_transition(trigger="shoulder_detection_failed", source="determine_injection_location", dest="error")
        self.state_machine.add_transition(trigger="vaccine_picked_up", source="vaccine_retrieval", dest="vaccine_delivery")
        self.state_machine.add_transition(trigger="vaccine_pickup_failed", source="vaccine_retrieval", dest="error")
        self.state_machine.add_transition(trigger="vaccine_delivered", source="vaccine_delivery", dest="vaccine_disposal")
        self.state_machine.add_transition(trigger="vaccive_delivery_failed", source="vaccine_delivery", dest="error")
        self.state_machine.add_transition(trigger="vaccine_disposed", source="vaccine_disposal", dest="idle")
        self.state_machine.add_transition(trigger="vaccine_disposal_failed", source="vaccine_disposal", dest="error")
        self.state_machine.add_transition(trigger="error_cleared", source="error", dest="idle")

        # wiring side effects to states
        self.state_machine.on_enter_determine_injection_location("determine_injection_location")
        self.state_machine.on_enter_vaccine_retrieval("vaccine_pickup")
        self.state_machine.on_enter_vaccine_delivery("vaccine_delivery")
        self.state_machine.on_enter_vaccine_disposal("vaccine_disposal")

        self.marlin_client = marlin_client
        self.gpio_client = gpio_client

        # setting injection location to a dummy value
        self.injection_location = (-1, -1)

    def set_injection_location(self, location):
        self.injection_location = location
        print(f"New injection location: {location}")

    def get_current_state(self):
        return self.state

    # side effect functions
    def determine_injection_location(self):
        if(verify_shoulder_location(self.injection_location)):
            print("Able to detect an injection location")
            self.shoulder_detected()
        else:
            print("Unable to detect an injection location")
            self.shoulder_detection_failed()

    def vaccine_pickup(self):
        self.marlin_client.home()
        if(self.gpio_client.get_breakbeam_sensor()):
            print("Vaccine detected on carriage")
            self.vaccine_picked_up()
        else:
            print("Vaccine not detected on carriage")
            self.vaccine_pickup_failed()

    def vaccine_delivery(self):
        injection_z = webcam_to_gantry(self.injection_location)
        self.marlin_client.move_to_position(100, injection_z)
        self.marlin_client.move_to_position(250, injection_z)
        self.gpio_client.engage_plunger()
        self.marlin_client.move_to_position(100, injection_z)
        self.gpio_client.retract_plunger()
        self.vaccine_delivered()

    def vaccine_disposal(self):
        self.marlin_client.move_to_position(0, 20)
        self.gpio_client.engage_disposal_mechanism()
        self.gpio_client.retract_disposal_mechanism()
        if(self.gpio_client.get_breakbeam_sensor()):
            print("Failed to dispose vaccine")
            self.vaccine_disposal_failed()
        else:
            print("Vaccine disposed successfully")
            self.vaccine_disposed()

    # event functions
    def send_injection_started(self):
        self.injection_started()

    def send_shoulder_detected(self):
        self.shoulder_detected()

    def send_shoulder_detection_failed(self):
        self.shoulder_detection_failed()

    def send_vaccine_picked_up(self):
        self.vaccine_picked_up()

    def send_vaccine_pickup_failed(self):
        self.vaccine_pickup_failed()

    def send_vaccine_delivered(self):
        self.vaccine_delivered()

    def send_vaccine_delivery_failed(self):
        self.vaccine_delivery_failed()

    def send_vaccine_disposed(self):
        self.vaccine_disposed()

    def send_vaccine_disposal_failed(self):
        self.vaccine_disposal_failed()

    def send_error_cleared(self):
        self.error_cleared()
