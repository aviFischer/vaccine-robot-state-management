from flask import Flask, request, jsonify

from state_machine import IVaccineRobot
from raspberrypi_gpio import IGpioClient

class FlaskApp:
    vaccine_robot: IVaccineRobot
    gpio_client: IGpioClient

    def __init__(self, vaccine_robot: IVaccineRobot, gpio_client: IGpioClient):
        self.vaccine_robot = vaccine_robot
        self.gpio_client = gpio_client

        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        self.app.route('/injection_location', methods=['POST'])(self.injection_location)
        self.app.route('/injection', methods=['POST'])(self.injection)
        self.app.route('/clear_error', methods=['POST'])(self.clear_error)
        self.app.route('/state', methods=['GET'])(self.get_state)

    def injection_location(self):
        data = request.form 
        x = int(data.get('x', None))
        y = int(data.get('y', None))

        if x == None or y == None:
            return "No injection location provided", 400

        self.vaccine_robot.set_injection_location((x, y))
        response = {'message': f'Injection location received: {(x, y)}'}
        return jsonify(response)
    
    # state machine endpoints
    def injection(self):
        if self.vaccine_robot.get_current_state() != "idle":
            return "Vaccine robot is not ready to run an injection", 409
        
        self.vaccine_robot.send_injection_started()
        response = {"message": "Running an injection"}
        return jsonify(response)
    
    def clear_error(self):
        if self.vaccine_robot.get_current_state() != "error":
            return "Vaccine robot must be in an error state to clear an error", 409
        
        self.vaccine_robot.send_error_cleared()
        response = {"message": "cleared the error"}
        return jsonify(response)

    def get_state(self):
        response = {"state": self.vaccine_robot.get_current_state()}
        return jsonify(response)
    
    # manual control endpoint
    def engage_plunger(self):
        self.gpio_client.engage_plunger()
        response = {"message": "Plunger extended"}
        return jsonify(response)
    
    def retract_plunger(self):
        self.gpio_client.retract_plunger()
        response = {"message": "Plunger retracted"}
        return jsonify(response)
    
    def engage_disposal(self):
        self.gpio_client.engage_disposal_mechanism()
        response = {"message": "Disposal mechanism extended"}
        return jsonify(response)
    
    def retract_disposal(self):
        self.gpio_client.retract_disposal_mechanism()
        response = {"message": "Disposal mechanism retracted"}
        return jsonify(response)

    def run(self):
        self.app.run(debug=True)
