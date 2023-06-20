# Find the distance between the object and the center of the screen

import board
import time
from math import sqrt
from circuitPyHuskyLib import HuskyLensLibrary

hl = HuskyLensLibrary('UART', TX=board.GP8, RX=board.GP9)
hl.algorithm("ALGORITHM_OBJECT_TRACKING") # Redirect to Object Tracking Function

def euclideanDist(p1, p2=(160,120)):
    x1,y1 = p1
    x2,y2 = p2
    print(p1)
    return sqrt((x1-x2)**2+(y1-y2)**2)

while True:
    results = hl.learnedBlocks() # Only get learned results
    
    if results: # if result not empty
        r = results[0]
        print(f"[{r.type}] (x:{r.x}, y:{r.y}), w:{r.width}, h:{r.height}")
        
        print(f"Distance to center: {euclideanDist((r.x,r.y))}")
    else:
        pass
    time.sleep(0.5)