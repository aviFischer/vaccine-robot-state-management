from flask_app import FlaskApp
from mocks import MockMarlinClient, MockGpioClient
from state_machine import VaccineRobot

# doing all initialization for the classes here (maybe switch to dependency injection)
def main():
    gpio_client = MockGpioClient()
    marlin_client = MockMarlinClient()
    vaccine_robot = VaccineRobot(marlin_client=marlin_client, gpio_client=gpio_client)
    flask_app = FlaskApp(vaccine_robot=vaccine_robot)

    flask_app.run()

if __name__ == "__main__":
    main()
