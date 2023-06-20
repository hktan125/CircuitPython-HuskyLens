import board
import time
import neopixel
from circuitPyHuskyLib import HuskyLensLibrary

hl = HuskyLensLibrary('UART', TX=board.GP8, RX=board.GP9)
hl.algorithm("ALGORITHM_FACE_RECOGNITION") # Redirect to Face Recognition Function

pixel = neopixel.NeoPixel(board.GP28, 1)

# Colors (r,g,b)
OFF = (0,0,0)
ON = (30,30,30)

# Assign different color to different ID
color = {1:(30,0,0),
         2:(0,30,0),
         3:(0,0,30)}

while True:
    try:
        results = hl.learnedBlocks() # Only get learned results (recognized face)
        
        if results: # if result not empty
            # Get all ID of recognized face on the screen
            all_id = list(set([result.ID for result in results])) 
            all_id.sort()
            print(f"All face ID: {all_id}")
            
            first = all_id[0] # Only take first face ID
            pixel.fill(color[first])
            print(f"ID: {first}")
        else:
            pixel.fill(OFF)
            
    except KeyError: # Handle if there is no color to be assigned to an ID
        pixel.fill(ON)
    
    finally:
        pixel.show()
        time.sleep(0.5)