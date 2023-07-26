import board
import busio
import digitalio
import adafruit_ssd1306
import time
from circuitPyHuskyLib import HuskyLensLibrary

oled_w, oled_h = 128, 64

i2c = busio.I2C(board.GP1, board.GP0)
oled = adafruit_ssd1306.SSD1306_I2C(oled_w, oled_h, i2c)

hl = HuskyLensLibrary('UART', TX=board.GP8, RX=board.GP9)
hl.verbose = False

def husky_2_oled(x, y, w, h):
    husky_w = 320
    husky_h = 240
    
    new_x = int((x/husky_w) * oled_w)
    new_w = int((w/husky_w) * oled_w)
    
    new_y = int((y/husky_h) * oled_h)
    new_h = int((h/husky_h) * oled_h)
    
    return new_x, new_y, new_w, new_h

def circle(r):
    #oled.fill(0)
    oled.circle(128//2, 64//2, r, 1)
    #oled.show()

r=1
hl.algorithm("ALGORITHM_OBJECT_TRACKING") # Redirect to Object Tracking Function
hl.clearText()
while True:
    oled.fill(0)
    
    results = hl.learnedBlocks() # Only get learned results
    
    if results: # if result not empty
        r = 1
        res = results[0]
        print(f"[{res.type}] (x:{res.x}, x_tl:{res.x_topleft}, y:{res.y}, y_tl:{res.y_topleft}), w:{res.width}, h:{res.height}")
        
        for result in results:
            x, y, w, h = husky_2_oled(result.x_topleft, result.y_topleft, result.width, result.height)
            oled.rect(x, y, w, h, 1)
        
    else:
        #oled.text('No object', 5, 5, 1, size=2)
        circle(r)
        r += 1
        if r > 64//2:
            r = 1
    
    oled.show()
    #time.sleep(0.5)
