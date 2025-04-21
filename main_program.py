import state_machine
import time
import scanning
import servos
import detection
import time 
import pd_controller

LOST_START_TIME =   0
retry =0
try:
    servos.GPIO_INIT()
    detection.VIDEO_INIT()
    pd_controller.init_pd()

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
                print("In PID state\n")
                res=detection.PROCESS_FRAME()
                if res[0]:
                    _,x,y=res #unpack X,Y coordinates of where frame was detected [T/F,x,y]
                    pan_pw, tilt_pw = pd_controller.update(x, y)
                elif not res[0]:
                    retry+=1
                if retry>5:
                    #start timer 5 second timer
                    LOST_START_TIME=current_time
                    #move to lost state
                    state_machine.current_state=state_machine.STATE_LOST
                    retry=0

            case state_machine.STATE_LOST:
                res=detection.PROCESS_FRAME()
                if res[0]:
                    state_machine.current_state=state_machine.STATE_DETECTED
                elif current_time-LOST_START_TIME>5:
                    state_machine.current_state=state_machine.STATE_SCANNING
            case _:
                break;

finally:
    detection.VIDEO_DEINIT()
    servos.GPIO_DEINIT()
