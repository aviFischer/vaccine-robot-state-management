from flask_app import FlaskApp
from raspberrypi_gpio import GPioClient
from gantry_movement import MarlinClient
from state_machine import VaccineRobot

# doing all initialization for the classes here (maybe switch to dependency injection)
def main():
    gpio_client = GPioClient.GpioClient()
    marlin_client = MarlinClient(com_port="/dev/ttyUSB0", baud_rate=250000)
    vaccine_robot = VaccineRobot(marlin_client=marlin_client, gpio_client=gpio_client)
    flask_app = FlaskApp(vaccine_robot=vaccine_robot)

    flask_app.run()

if __name__ == "__main__":
    main()
