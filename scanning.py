import scanning
import time

def SCAN():
    duty=scanning.PAN_MIN_DUTY
    step=0.2
    while True:
        PAN_PWM.ChangeDutyCycle(duty)
        time.sleep(0.05)

        
        if duty>=scanning.PAN_MAX_DUTY:
            step=-abs(step)
        elif duty<=scanning.PAN_MAX_DUTY:
            step=abs(step)
        
        duty+=step

