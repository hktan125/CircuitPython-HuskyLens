# Find the distance between the object and the center of the screen
# Find what is the position of the object on the screen

import board
import time
from math import sqrt
from circuitPyHuskyLib import HuskyLensLibrary

DIST_THRESHOLD = 20

hl = HuskyLensLibrary('UART', TX=board.GP8, RX=board.GP9)
hl.algorithm("ALGORITHM_OBJECT_TRACKING") # Redirect to Object Tracking Function

def euclideanDist(p1, p2=(160,120)):
    x1,y1 = p1
    x2,y2 = p2
    return sqrt((x1-x2)**2+(y1-y2)**2)

def findPosition(p1, p2=(160,120)):
    # object (x1,y1)
    # Center point (x2,y2)
    # y2 - y1 > 0, (positive/True) ==> [object position is above center]
    # y2 - y1 < 0, (negative/False) ==> [object position is below center]
    # same with x-axis
    x1,y1 = p1
    x2,y2 = p2
    
    x = x2-x1
    y = y2-y1
    
    return True if x>0 else False, True if y>0 else False

assert (DIST_THRESHOLD > 0), "min DIST_THRESHOLD is 1"
while True:
    results = hl.learnedBlocks() # Only get learned results
    
    if results: # if result not empty
        r = results[0]
        print(f"[{r.type}] (x:{r.x}, y:{r.y}), w:{r.width}, h:{r.height}")
        
        dist = euclideanDist((r.x,r.y))
        
        print(f"Distance to center: {dist}")
        
        if dist > DIST_THRESHOLD:
            print(f"{findPosition((r.x, r.y))}")
            
    time.sleep(0.5)