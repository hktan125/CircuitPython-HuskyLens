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

while True:
    results = hl.blocks() # Get All type=BLOCK result
    
    if results: # if result not empty
        print(f"Detected face count: {len(results)}")
        pixel.fill(ON)
    else:
        pixel.fill(OFF)
        
    pixel.show()
    time.sleep(0.5)