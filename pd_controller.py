# pd_controller.py

import time
import servos
import detection

# PD gains – tune these!
KP_PAN  =  0.05   # proportional gain for pan
KD_PAN  =  0.02   # derivative gain for pan
KP_TILT =  0.05   # proportional gain for tilt
KD_TILT =  0.02   # derivative gain for tilt

# state for D term
_last_pan_error  = 0.0
_last_tilt_error = 0.0
_last_time       = None

def init_pd():
    """Initialize/reset the PD controller state (call once at startup)."""
    global _last_time, _last_pan_error, _last_tilt_error
    _last_time       = time.monotonic()
    _last_pan_error  = 0.0
    _last_tilt_error = 0.0

def update(x, y):
    """
    Run one PD update.
    
    Args:
      x, y: pixel coordinates of target in the frame.

    Returns:
      (new_pan_pw, new_tilt_pw): the PWM values just sent to the servos.
    """
    global _last_pan_error, _last_tilt_error, _last_time

    
    now = time.monotonic()                                      #get current time
    dt  = now - _last_time if _last_time is not None else 0.0   #get last time if second occurance otherwise it will use 0
    _last_time = now                            

    #compute error
    dx = x - (detection.CAMERA_WIDTH  / 2)      #x error from center
    dy = y - (detection.CAMERA_HEIGHT / 2)      #y error from center

    pan_error  =  -dx / (detection.CAMERA_WIDTH  / 2) * (detection.HORIZONTAL_FOV / 2)  #normalize x error (pan) to current frame (in degrees)
    tilt_error = dy / (detection.CAMERA_HEIGHT / 2) * (detection.VERTICAL_FOV   / 2)    #normalize y error (tilt) to current frame (in degrees)

   #Proportial control for pan/tilt
    pan_p_term  = KP_PAN  * pan_error
    tilt_p_term = KP_TILT * tilt_error

    #Derivative control for pan/tilt
    pan_d_term  = KD_PAN  * ((pan_error  - _last_pan_error)  / dt if dt > 0 else 0.0) 
    tilt_d_term = KD_TILT * ((tilt_error - _last_tilt_error) / dt if dt > 0 else 0.0)

    #Update old error with new error for next iteration
    _last_pan_error  = pan_error
    _last_tilt_error = tilt_error

    #total control for pan and tilt (in degrees)
    pan_control  = pan_p_term  + pan_d_term
    tilt_control = tilt_p_term + tilt_d_term

    #read current angle of pan/tilt servos
    current_pan_angle  = servos.pwm_to_angle(
        servos.get_pan_pwm(),
        servos.PAN_MIN_PW, servos.PAN_MAX_PW,
        servos.PAN_MIN_ANGLE, servos.PAN_MAX_ANGLE
    )
    current_tilt_angle = servos.pwm_to_angle(
        servos.get_tilt_pwm(),
        servos.TILT_MIN_PW, servos.TILT_MAX_PW,
        servos.TILT_MIN_ANGLE, servos.TILT_MAX_ANGLE
    )

    #Compute the new angles relative to the current position of servos
    new_pan_angle  = max(servos.PAN_MIN_ANGLE,  min(servos.PAN_MAX_ANGLE,  current_pan_angle  + pan_control))
    new_tilt_angle = max(servos.TILT_MIN_ANGLE, min(servos.TILT_MAX_ANGLE, current_tilt_angle + tilt_control))

    #Convert angle to pwm
    new_pan_pw  = servos.angle_to_pwm(
        new_pan_angle, servos.PAN_MIN_PW, servos.PAN_MAX_PW,
        servos.PAN_MIN_ANGLE, servos.PAN_MAX_ANGLE
    )
    new_tilt_pw = servos.angle_to_pwm(
        new_tilt_angle, servos.TILT_MIN_PW, servos.TILT_MAX_PW,
        servos.TILT_MIN_ANGLE, servos.TILT_MAX_ANGLE
    )

    #Apply pwm of servos
    servos.set_pan_pulsewidth(new_pan_pw)
    servos.set_tilt_pulsewidth(new_tilt_pw)

    return new_pan_pw, new_tilt_pw
