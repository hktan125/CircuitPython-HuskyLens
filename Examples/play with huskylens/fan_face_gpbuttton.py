import board
import digitalio
import time
from circuitPyHuskyLib import HuskyLensLibrary

hl = HuskyLensLibrary('UART', TX=board.GP8, RX=board.GP9)
hl.algorithm("ALGORITHM_FACE_RECOGNITION") # Redirect to Face Recognition Function

fan = digitalio.DigitalInOut(board.GP27)
fan.direction = digitalio.Direction.OUTPUT

# Button to change mode
gp20 = digitalio.DigitalInOut(board.GP20)
gp20.direction = digitalio.Direction.INPUT

# Button to learn face
gp21 = digitalio.DigitalInOut(board.GP21)
gp21.direction = digitalio.Direction.INPUT

# Button to forget
gp22 = digitalio.DigitalInOut(board.GP22)
gp22.direction = digitalio.Direction.INPUT

RECOG=False
hl.customText('All face mode',20,20)
hl.forget()

while True:
    if gp20.value == False:
        RECOG = not RECOG
        hl.clearText()
        if RECOG:
            hl.customText('Recognition mode',20,20)
        else:
            hl.customText('All face mode',20,20)
            hl.forget()
    
    if RECOG:
        if gp21.value == False:
            hl.learn(10) # Set id = 10 when learning face
        if gp22.value == False:
            hl.forget()
        
        results = hl.learnedBlocks() # Only get learned results (recognized face)
        
        if results: # if result not empty
            # Get all ID of recognized face on the screen
            all_id = list(set([result.ID for result in results]))
            
            # If id = 10 is found, turn on the fan
            if 10 in all_id:
                fan.value = True
            else:
                fan.value = False
        
    else:
        results = hl.blocks() # Only get learned results (recognized face)
        
        if results: # if result not empty
            fan.value = True
    
    if not results:
        fan.value = False
    
    time.sleep(0.5)

