import board
import time
import neopixel
from circuitPyHuskyLib import HuskyLensLibrary

hl = HuskyLensLibrary('UART', TX=board.GP8, RX=board.GP9)
hl.algorithm("ALGORITHM_LINE_TRACKING") # Redirect to Line Tracking Function

pixel = neopixel.NeoPixel(board.GP28, 1)

# Colors (r,g,b)
OFF = (0,0,0)
ON = (30,30,30)

while True:
    results = hl.learnedArrows() # Only get learned results
    
    if results: # if result not empty
        pixel.fill(ON)
        r = results[0]
        print(f"[{r.type}] Head:(x:{r.xHead}, y:{r.yHead}), Tail:(x:{r.xTail}, y:{r.yTail})")
    else:
        pixel.fill(OFF)
    
    pixel.show()    
    time.sleep(0.5)