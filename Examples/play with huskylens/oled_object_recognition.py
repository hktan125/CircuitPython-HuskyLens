import board
import time
import busio
import adafruit_ssd1306
from circuitPyHuskyLib import HuskyLensLibrary

hl = HuskyLensLibrary('UART', TX=board.GP8, RX=board.GP9)
hl.algorithm("ALGORITHM_OBJECT_RECOGNITION") # Redirect to Object Recognition Function

i2c = busio.I2C(board.GP1, board.GP0)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# https://www.dfrobot.com/forum/topic/28187
# You need to learn and manually map id to the object
id_and_name = {1: 'potted\nplant',
               2: 'car',
               3: 'aeroplane',}

while True:
    oled.fill(0)
    try:
        results = hl.learnedBlocks() # Only get learned results
        
        if results: # if result not empty
            r = results[0]
            print(f"ID: {r.ID}, {id_and_name[r.ID]}")
            oled.text(f"{id_and_name[r.ID]}", 5, 5, 1, size=2)
        else:
            oled.text('No object', 5, 5, 1, size=2)
            
    except KeyError: # Handle if there is no color to be assigned to an ID
        oled.text('Please manually\nmap ID to name', 5, 0, 1)
    finally:
        oled.show()
        