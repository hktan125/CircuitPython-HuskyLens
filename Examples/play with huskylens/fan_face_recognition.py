import board
import digitalio
import time
from circuitPyHuskyLib import HuskyLensLibrary

hl = HuskyLensLibrary('UART', TX=board.GP8, RX=board.GP9)
hl.algorithm("ALGORITHM_FACE_RECOGNITION") # Redirect to Face Recognition Function

fan = digitalio.DigitalInOut(board.GP27)
fan.direction = digitalio.Direction.OUTPUT

while True:
    results = hl.learnedBlocks() # Only get learned results (recognized face)
        
    if results: # if result not empty
        # Get all ID of recognized face on the screen
        all_id = list(set([result.ID for result in results]))
        all_id.sort()
        print(f"All face ID: {all_id}")
        
        # If id = 1 is found, turn on the fan
        if 1 in all_id:
            fan.value = True
        else:
            fan.value = False
    else:
        fan.value = False
    
    time.sleep(0.5)