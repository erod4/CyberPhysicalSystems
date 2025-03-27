import servos
import time
import detection
import state_machine

def SCAN():
    """
    Perform one scan update of the pan servo between PAN_MIN_PW and PAN_MAX_PW.
    The pulse and step values persist across function calls.
    """
 # init static variables
    if not hasattr(SCAN, "pulse"):
        SCAN.pulse = servos.PAN_MIN_PW
    if not hasattr(SCAN, "step"):
        SCAN.step = 15  
    
    # update the servo position with the current pulse value
    servos.set_pan_pulsewidth(SCAN.pulse)

    #process current frame
    detection_found,x,y = detection.PROCESS_FRAME()

    #if detected FSM will change state
    if detection_found:
        return True
    time.sleep(0.09)

    # Adjust the pulse value and reverse direction if limits are reached
    if SCAN.pulse + SCAN.step > servos.PAN_MAX_PW:
        SCAN.pulse = servos.PAN_MAX_PW
        SCAN.step = -abs(SCAN.step)
    elif SCAN.pulse + SCAN.step < servos.PAN_MIN_PW:
        SCAN.pulse = servos.PAN_MIN_PW
        SCAN.step = abs(SCAN.step)
    else:
        SCAN.pulse += SCAN.step

    return False
    

