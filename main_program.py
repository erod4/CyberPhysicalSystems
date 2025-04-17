import state_machine
import time
import scanning
import servos
import detection
import time 

LOST_START_TIME =   0

try:
    servos.GPIO_INIT()
    detection.VIDEO_INIT()
    while True:
        current_time = time.monotonic() 
        match state_machine.current_state:
            case state_machine.STATE_INIT:
                print("In Init State\n")
                state_machine.current_state=state_machine.STATE_SCANNING
            case state_machine.STATE_SCANNING:
                print("In Scanning State\n")
                #scans until object is detected then starts pid to track object
                if scanning.SCAN(): #scanning.SCAN() moves the pan servo then checks a frame for a detection (if detection occurs it returns true otherwise false)
                    state_machine.current_state=state_machine.STATE_DETECTED
            case state_machine.STATE_DETECTED:
                #PID to track object
                print("start PID\n")
                if detection.PROCESS_FRAME()[0]:
                    # _,x,y=detection.PROCESS_FRAME() #unpack X,Y coordinates of where frame was detected [T/F,x,y]
                    # print("x: ",x)
                    # print("y: ",y)
                    # pan_pwm,tilt_pwm=servos.coordinates_to_pw(x,y)
                    # servos.set_pan_pulsewidth(pan_pwm)
                    # servos.set_tilt_pulsewidth(tilt_pwm)
                    # time.sleep(5)
                    pass
                    #update PID controller
                else:
                    #start timer 5 second timer
                    LOST_START_TIME=current_time
                    #move to lost state
                    state_machine.current_state=state_machine.STATE_LOST

            case state_machine.STATE_LOST:
                if detection.PROCESS_FRAME()[0]:
                    state_machine.current_state=state_machine.STATE_DETECTED
                elif current_time-LOST_START_TIME<5:
                    #keep trying PID until frame is detected or timer hits 5 seconds
                    pass
                else:
                    #time ellapsed move back to scanning 
                    state_machine.current_state=state_machine.STATE_SCANNING
            case _:
                break;

finally:
    detection.VIDEO_DEINIT()
    servos.GPIO_DEINIT()
