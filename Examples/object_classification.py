import board
import time
import neopixel
from circuitPyHuskyLib import HuskyLensLibrary

hl = HuskyLensLibrary('UART', TX=board.GP8, RX=board.GP9)
hl.algorithm("ALGORITHM_OBJECT_CLASSIFICATION") # Redirect to Object Classification Function

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
        results = hl.learnedBlocks() # Only get learned results
        
        if results: # if result not empty
            r = results[0]
            pixel.fill(color[r.ID])
            print(f"ID: {r.ID}")
        else:
            pixel.fill(OFF)
            
    except KeyError: # Handle if there is no color to be assigned to an ID
        pixel.fill(ON)
    
    finally:
        pixel.show()
        time.sleep(0.5)