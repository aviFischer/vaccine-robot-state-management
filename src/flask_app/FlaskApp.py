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

    def injection_location(self):
        data = request.json 
        location = data.get('location', None)

        if not location:
            return "No injection location provided", 400

        self.vaccine_robot.set_injection_location(location)
        response = {'message': f'Injection location received: {location}'}
        return jsonify(response)

    def injection(self):
        data = request.json  # Assuming the data is sent in JSON format
        # Your logic for injection endpoint here
        injection_data = data.get('injection_data', 'No Injection Data')
        response = {'message': f'Injection data received: {injection_data}'}
        return jsonify(response)

    def run(self):
        self.app.run(debug=True)
