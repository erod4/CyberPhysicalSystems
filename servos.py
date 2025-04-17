import pigpio
import time
import detection

PAN_GPIO=17
TILT_GPIO=27

PAN_MIN_PW = 500
PAN_MAX_PW = 2500
TILT_MIN_PW=833
TILT_MAX_PW=1667


pan_center=(PAN_MIN_PW+PAN_MAX_PW)/2
tilt_center=(TILT_MIN_PW+TILT_MAX_PW)/2

pi = None


def GPIO_INIT():
    global pi
    pi = pigpio.pi()
    if not pi.connected:
        raise Exception("Could not connect to pigpio daemon!")
    SERVO_CALIBRATION()


def SERVO_CALIBRATION():
    global pan_center, tilt_center
    pi.set_servo_pulsewidth(PAN_GPIO, pan_center)
    pi.set_servo_pulsewidth(TILT_GPIO, tilt_center)

    time.sleep(0.5) 


def set_pan_pulsewidth(pw):
    """Set the pulse width for the pan servo."""
    pi.set_servo_pulsewidth(PAN_GPIO, pw)
def set_tilt_pulsewidth(pw):
    """Set the pulse width for the pan servo."""
    pi.set_servo_pulsewidth(TILT_GPIO, pw)
    
def coordinates_to_pw(x,y):
    global pan_center, tilt_center

    #normalize x,y cordinates between [-1,1]
    normalized_x=(x-detection.CAMERA_WIDTH/2)/(detection.CAMERA_WIDTH/2)
    normalized_y=(y-detection.CAMERA_HEIGHT/2)/(detection.CAMERA_HEIGHT/2)

    #normalize coordinates to servo pw
    
    pan_pwm=normalized_x*(PAN_MAX_PW-PAN_MIN_PW)+pan_center
    tilt_pwm=normalized_y*(TILT_MAX_PW-TILT_MIN_PW)+tilt_center
    print("PAN PWM: ",pan_pwm)
    print("TILT PWM: ", tilt_pwm)
    return [pan_pwm,tilt_pwm]
    
def GPIO_DEINIT():
    pi.set_PWM_dutycycle(PAN_GPIO,0)
    pi.set_PWM_dutycycle(TILT_GPIO,0)
    pi.stop()
    
