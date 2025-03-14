import state_machine
import time
import scanning

try:
    while True:
        if state_machine.current_state==state_machine.STATE_INIT:
            print("In Init State\n")
            state_machine.current_state=state_machine.STATE_SCANNING
        if state_machine.current_state==state_machine.STATE_SCANNING:
            print("In Scanning State\n")
            break

finally:
    pass