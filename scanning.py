import servos
import time
import detection
import state_machine

def SCAN():
    """
    Continuously scan the pan servo between PAN_MIN_PW and PAN_MAX_PW.
    Adjust the step value for smoother or faster movement.
    """
    pulse = servos.PAN_MIN_PW
    step = 15  # Pulse width step in microseconds; smaller step yields smoother movement
    while True:
        servos.set_pan_pulsewidth(pulse)
        # Process the current frame (or perform your detection task)
        if(detection.PROCESS_FRAME()[0]):
            #if object is detected move to state detected state (tracking/PID controller)
            state_machine.current_state=state_machine.STATE_DETECTED
            return
        time.sleep(0.09)
        # Reverse direction when limits are reached
        if step+pulse>servos.PAN_MAX_PW:
            pulse=servos.PAN_MAX_PW
            step=-abs(step)
            pass
        elif step+pulse<servos.PAN_MIN_PW:
            pulse=servos.PAN_MIN_PW
            step=abs(step)
        else:
            pulse+=step


