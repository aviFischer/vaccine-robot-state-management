from flask import Flask, request, jsonify

from state_machine import IVaccineRobot

class FlaskApp:
    vaccine_robot: IVaccineRobot

    def __init__(self, vaccine_robot: IVaccineRobot):
        self.vaccine_robot = vaccine_robot

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

    def run(self):
        self.app.run(debug=True)
