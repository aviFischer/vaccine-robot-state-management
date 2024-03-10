try:
    import RPi.GPIO as GPIO # this library only works on raspbian
except Exception as e:
    pass
import time

from .IGpioClient import IGpioClient

PLUNGER_IN1 = 11
PLUNGER_IN2 = 13
DISPOSAL_IN1 = 16
DISPOSAL_IN2 = 18

BREAKBEAM_READ = 29

PUSHROD_DELAY_TIME = 8 # calculated as 50 mm / 7 mm/s rounded up

class GpioClient(IGpioClient):

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PLUNGER_IN1, GPIO.OUT)
        GPIO.setup(PLUNGER_IN2, GPIO.OUT)
        GPIO.setup(DISPOSAL_IN1, GPIO.OUT)
        GPIO.setup(DISPOSAL_IN2, GPIO.OUT)
        GPIO.setup(BREAKBEAM_READ, GPIO.IN)

    def get_breakbeam_sensor(self) -> int:
        return GPIO.input(BREAKBEAM_READ)

    def engage_disposal_mechanism(self):
        GPIO.output(DISPOSAL_IN1, GPIO.HIGH)
        GPIO.output(DISPOSAL_IN2, GPIO.LOW)

        time.sleep(8)

        GPIO.output(DISPOSAL_IN1, GPIO.LOW)
        GPIO.output(DISPOSAL_IN2, GPIO.LOW)

    def retract_disposal_mechanism(self):
        GPIO.output(DISPOSAL_IN1, GPIO.LOW)
        GPIO.output(DISPOSAL_IN2, GPIO.HIGH)

        time.sleep(8)

        GPIO.output(DISPOSAL_IN1, GPIO.LOW)
        GPIO.output(DISPOSAL_IN2, GPIO.LOW)
        
    def engage_plunger(self):
        GPIO.output(PLUNGER_IN1, GPIO.HIGH)
        GPIO.output(PLUNGER_IN2, GPIO.LOW)

        time.sleep(8)

        GPIO.output(PLUNGER_IN1, GPIO.LOW)
        GPIO.output(PLUNGER_IN2, GPIO.LOW)

    def retract_plunger(self):
        GPIO.output(PLUNGER_IN1, GPIO.LOW)
        GPIO.output(PLUNGER_IN2, GPIO.HIGH)

        time.sleep(8)

        GPIO.output(PLUNGER_IN1, GPIO.LOW)
        GPIO.output(PLUNGER_IN2, GPIO.LOW)
