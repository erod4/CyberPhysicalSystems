import state_machine
import time
import scanning
import servos
import detection

try:
    servos.GPIO_INIT()
    detection.VIDEO_INIT()
    while True:
        if state_machine.current_state==state_machine.STATE_INIT:
            print("In Init State\n")
            state_machine.current_state=state_machine.STATE_SCANNING
        if state_machine.current_state==state_machine.STATE_SCANNING:
            print("In Scanning State\n")
            scanning.SCAN()

finally:
    detection.VIDEO_DEINIT()