import board
import time
import neopixel
from circuitPyHuskyLib import HuskyLensLibrary

hl = HuskyLensLibrary('UART', TX=board.GP8, RX=board.GP9)
hl.algorithm("ALGORITHM_OBJECT_TRACKING") # Redirect to Object Tracking Function

pixel = neopixel.NeoPixel(board.GP28, 1)

# Colors (r,g,b)
OFF = (0,0,0)
ON = (30,30,30)

while True:
    results = hl.learnedBlocks() # Only get learned results
    
    if results: # if result not empty
        pixel.fill(ON)
        r = results[0]
        print(f"[{r.type}] (x:{r.x}, y:{r.y}), w:{r.width}, h:{r.height}")
    else:
        pixel.fill(OFF)
    
    pixel.show()    
    time.sleep(0.5)