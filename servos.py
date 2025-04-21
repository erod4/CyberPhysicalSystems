import pigpio
import time
import detection

PAN_GPIO=17
TILT_GPIO=27

PAN_MIN_PW = 500
PAN_MAX_PW = 2500
TILT_MIN_PW=1900
TILT_MAX_PW=2500

PAN_MIN_ANGLE=0
PAN_MAX_ANGLE=180
TILT_MIN_ANGLE=136
TILT_MAX_ANGLE=180

pan_center=(PAN_MIN_PW+PAN_MAX_PW)/2
tilt_center=(TILT_MIN_PW+TILT_MAX_PW)/2

pi = None


def GPIO_INIT():
    global pi
    pi = pigpio.pi()
    if not pi.connected:
        raise Exception("Could not connect to pigpio daemon!")
    SERVO_CALIBRATION()

def get_pan_pwm():
    return pi.get_servo_pulsewidth(PAN_GPIO)

def get_tilt_pwm():
    return pi.get_servo_pulsewidth(TILT_GPIO)

def SERVO_CALIBRATION():
    global pan_center, tilt_center
    pi.set_servo_pulsewidth(PAN_GPIO, int(pan_center))
    pi.set_servo_pulsewidth(TILT_GPIO, int(tilt_center))
    print(f"pan_center: {pan_center}, tilt_center:{tilt_center}\r\n")
    time.sleep(0.5) 


def set_pan_pulsewidth(pw):
    """Set the pulse width for the pan servo."""
    pi.set_servo_pulsewidth(PAN_GPIO, pw)
def set_tilt_pulsewidth(pw):
    """Set the pulse width for the pan servo."""
    pi.set_servo_pulsewidth(TILT_GPIO, pw)
    
def pwm_to_angle(pulse_width, min_pw=500,max_pw=2500, min_angle=0, max_angle=180):
    if(pulse_width<min_pw or pulse_width>max_pw):
        return None
    angle = (pulse_width - min_pw) * (max_angle - min_angle) / (max_pw - min_pw) + min_angle
    return angle
def angle_to_pwm(angle, min_pw=500, max_pw=2500,min_angle=0, max_angle=180):
    # Clamp angle to valid range
    angle = max(min_angle, min(max_angle, angle))
    pwm = (angle - min_angle) * (max_pw - min_pw) / (max_angle - min_angle) + min_pw
    return int(pwm)

def coordinates_to_pw(x,y):
    #get pan/tilt pwm
    pan_pw=get_pan_pwm()
    tilt_pw=get_tilt_pwm()

    #convert to angle
    current_pan_angle=pwm_to_angle(pan_pw,PAN_MIN_PW,PAN_MAX_PW,PAN_MIN_ANGLE,PAN_MAX_ANGLE)
    current_tilt_angle=pwm_to_angle(tilt_pw,TILT_MIN_PW,TILT_MAX_PW,TILT_MIN_ANGLE,TILT_MAX_ANGLE)

    #calculate distance from center of the screen
    dx=x-(detection.CAMERA_WIDTH/2)
    dy=y-(detection.CAMERA_HEIGHT/2)

    #normalize between [-1,1]
    nx=dx/(detection.CAMERA_WIDTH/2)
    ny=dy/(detection.CAMERA_HEIGHT/2)

    pan_offset=nx*(detection.HORIZONTAL_FOV/2)
    tilt_offset=-ny*(detection.VERTICAL_FOV/2)

    new_pan=current_pan_angle+pan_offset
    new_tilt=current_tilt_angle+tilt_offset

    #clamp between angle range
    new_pan=max(PAN_MIN_ANGLE,min(PAN_MAX_ANGLE,new_pan))
    new_tilt=max(TILT_MIN_ANGLE,min(TILT_MAX_ANGLE,new_tilt))

    #convert angle to pwm
    new_pan_pw=angle_to_pwm(new_pan,PAN_MIN_PW,PAN_MAX_PW,PAN_MIN_ANGLE,PAN_MAX_ANGLE)
    new_tilt_pw=angle_to_pwm(new_tilt,TILT_MIN_PW,TILT_MAX_PW,TILT_MIN_ANGLE,TILT_MAX_ANGLE)
    print(f"Target X,Y: {x},{y}")
    print(f"New pan angle: {new_pan}, New tilt angle: {new_tilt}")
    print(f"New PWM: pan={new_pan_pw}, tilt={new_tilt_pw}")
    return [new_pan_pw,new_tilt_pw]
    
def GPIO_DEINIT():
    pi.set_PWM_dutycycle(PAN_GPIO,0)
    pi.set_PWM_dutycycle(TILT_GPIO,0)
    pi.stop()
    
