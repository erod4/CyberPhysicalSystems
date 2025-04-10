import state_machine
import time
import scanning
import servos
import detection
import time 
try:
    servos.GPIO_INIT()
    detection.VIDEO_INIT()
    while True:
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
                x_cord,y_coord
                if detection.PROCESS_FRAME():
                    _,x,y=detection.PROCESS_FRAME() #unpack X,Y coordinates of where frame was detected
                    #update PID controller
                else:
                    #start timer 5 second timer

                    #move to lost state


                print("start PID\n")
            case _:
                break;

finally:
    detection.VIDEO_DEINIT()