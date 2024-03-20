import time
from flask import Flask, request, jsonify, Response

from state_machine import IVaccineRobot
from raspberrypi_gpio import IGpioClient
from gantry_movement import IMarlinClient

class FlaskApp:
    vaccine_robot: IVaccineRobot
    gpio_client: IGpioClient
    marlin_client: IMarlinClient

    def __init__(self, vaccine_robot: IVaccineRobot, gpio_client: IGpioClient, marlin_client: IMarlinClient):
        self.vaccine_robot = vaccine_robot
        self.gpio_client = gpio_client
        self.marlin_client = marlin_client

        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        self.app.route("/injection_location", methods=["POST"])(self.injection_location)
        self.app.route("/injection", methods=["POST"])(self.injection)
        self.app.route("/clear_error", methods=["POST"])(self.clear_error)
        self.app.route("/state", methods=["GET"])(self.get_state)
        self.app.route("/engage_plunger", methods=["POST"])(self.engage_plunger)
        self.app.route("/retract_plunger", methods=["POST"])(self.retract_plunger)
        self.app.route("/engage_disposal", methods=["POST"])(self.engage_disposal)
        self.app.route("/retract_disposal", methods=["POST"])(self.retract_disposal)
        self.app.route("/home", methods=["POST"])(self.home)
        self.app.route("/ir_sensor", methods=["GET"])(self.get_IR_sensor)
        self.app.route("/state_stream", methods=["GET"])(self.state_stream)
        self.app.route("/move_to_shoulder", methods=["POST"])(self.move_to_shoulder)

    def injection_location(self):
        data = request.json
        left_x = int(data.get("left_x", None))
        left_y = int(data.get("left_y", None))
        right_x = int(data.get("right_x", None))
        right_y = int(data.get("right_y", None))

        if left_x == None or left_y == None or right_x == None or right_y == None:
            return "No injection location provided", 400

        # Assuming left shoulder only for now
        self.vaccine_robot.set_injection_location((left_x, left_y))
        response = {"message": f"Injection location received: {(left_x, left_y)}"}
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
        response = jsonify({"state": self.vaccine_robot.get_current_state()})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    
    def state_stream(self):
        def stream():
            while True:
                yield self.vaccine_robot.get_current_state()   
                time.sleep(1)

        return Response(stream(), mimetype='text/event-stream')
    
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
    
    def home(self):
        self.marlin_client.home()
        response = {"message": "Gantry Homed"}
        return jsonify(response)
    
    def get_IR_sensor(self):
        reading = self.gpio_client.get_breakbeam_sensor()
        response = jsonify({"Sensor value": reading})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    
    def move_to_shoulder(self):
        self.vaccine_robot.move_to_shoulder()

    def run(self):
        self.app.run(debug=True)
