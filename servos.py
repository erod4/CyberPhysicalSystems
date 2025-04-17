import pigpio
import time
import detetion

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
    time.sleep(0.5) 


def set_pan_pulsewidth(pw):
    """Set the pulse width for the pan servo."""
    pi.set_servo_pulsewidth(PAN_GPIO, pw)

def coordinates_to_pw(x,y):
    #normalize x,y cordinates between [-1,1]
    normalized_x=(x-detection.CAMERA_WIDTH/2)/(detection.CAMERA_WIDTH/2)
    normalized_x=(y-detection.CAMERA_HEIGHT/2)/(detection.CAMERA_HEIGHT/2)

    #normalize coordinates to servo pw
    pan_angle=normalized_x*PAN_
