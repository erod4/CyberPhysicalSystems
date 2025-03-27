import pigpio
import time


PAN_GPIO=27
TILT_GPIO=17

PAN_MIN_PW = 500
PAN_MAX_PW = 2500

pi = None


def GPIO_INIT():
    global pi
    pi = pigpio.pi()
    if not pi.connected:
        raise Exception("Could not connect to pigpio daemon!")
    SERVO_CALIBRATION()


def SERVO_CALIBRATION():
    pi.set_servo_pulsewidth(PAN_GPIO, PAN_MIN_PW)
    # pi.set_servo_pulsewidth(TILT_GPIO, TILT_MIN_PW)
    time.sleep(0.5)  # Allow time for the servos to reach the position


def set_pan_pulsewidth(pw):
    """Set the pulse width for the pan servo."""
    pi.set_servo_pulsewidth(PAN_GPIO, pw)
