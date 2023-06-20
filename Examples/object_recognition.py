import board
import time
import neopixel
from circuitPyHuskyLib import HuskyLensLibrary

hl = HuskyLensLibrary('UART', TX=board.GP8, RX=board.GP9)
hl.algorithm("ALGORITHM_OBJECT_RECOGNITION") # Redirect to Object Recognition Function

pixel = neopixel.NeoPixel(board.GP28, 1)

# Colors (r,g,b)
OFF = (0,0,0)
ON = (30,30,30)

# Assign different color to different ID
color = {1:(30,0,0),
         2:(0,30,0),
         3:(0,0,30)}

# https://www.dfrobot.com/forum/topic/28187
# You need to learn and manually map id to the object
id_and_name = {1: 'pottedplant',
               2: 'car',
               3: 'aeroplane',}

while True:
    try:
        results = hl.learnedBlocks() # Only get learned results
        
        if results: # if result not empty
            
            first = results[0].ID # Only take first ID
            pixel.fill(color[first])
            
            print(f"ID: {first}, Name: {id_and_name[first]}")
        else:
            pixel.fill(OFF)
            
    except KeyError: # Handle if there is no color to be assigned to an ID
        pixel.fill(ON)
        print(f"ID: {first}, Name: [refer to line 22]")
    
    finally:
        pixel.show()
        time.sleep(0.5)