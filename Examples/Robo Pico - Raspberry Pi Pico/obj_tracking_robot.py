# obj_tracking_robot.py

import time
import board
import digitalio
import pwmio
from math import sqrt
from adafruit_motor import motor

from circuitPyHuskyLib import HuskyLensLibrary

DIST_THRESHOLD = 30
SPEED = 0.3
MOVE = True

hl = HuskyLensLibrary('UART', TX=board.GP12, RX=board.GP13)
hl.algorithm("ALGORITHM_OBJECT_TRACKING") # Redirect to object tracking

# Left Motor
PWM_M1A = board.GP8
PWM_M1B = board.GP9
# Right Motor
PWM_M2A = board.GP10
PWM_M2B = board.GP11

# DC motor setup
# DC Motors generate electrical noise when running that can reset the microcontroller in extreme
# cases. A capacitor can be used to help prevent this.
pwm_1a = pwmio.PWMOut(PWM_M1A, frequency=10000)
pwm_1b = pwmio.PWMOut(PWM_M1B, frequency=10000)
motorL = motor.DCMotor(pwm_1a, pwm_1b)
pwm_2a = pwmio.PWMOut(PWM_M2A, frequency=10000)
pwm_2b = pwmio.PWMOut(PWM_M2B, frequency=10000)
motorR = motor.DCMotor(pwm_2a, pwm_2b)

gp20 = digitalio.DigitalInOut(board.GP20)
gp20.direction = digitalio.Direction.INPUT

def Robot_Movement(sL, sR):
    motorL.throttle = sL
    motorR.throttle = sR

def euclideanDist(p1, p2=(160,120)):
    x1,y1 = p1
    x2,y2 = p2
    return sqrt((x1-x2)**2+(y1-y2)**2)

def findVerticalPos(p1, p2=(160,120)):
    # object (x1,y1)
    # Center point (x2,y2)
    # y2 - y1 > 0, (positive/FRONT) ==> [object position is above center]
    # y2 - y1 < 0, (negative/BACK) ==> [object position is below center]
    _, y1 = p1
    _, y2 = p2
    y = y2-y1
    
    return euclideanDist((0,y1),(0,y2)) > DIST_THRESHOLD, 'FRONT' if y>0 else 'BACK'

def findHorizontalPos(p1, p2=(160,120)):
    # x2 - x1 > 0, (positive/LEFT) ==> [object position is less than center]
    # x2 - x1 < 0, (negative/RIGHT) ==> [object position is more than center]
    x1, _ = p1
    x2, _ = p2
    x = x2-x1
    
    return euclideanDist((x1,0),(x2,0)) > DIST_THRESHOLD, 'LEFT' if x>0 else 'RIGHT'

def getVelocity(direction, speed=SPEED):
    VELOCITY = {
        'FRONT': (speed,speed),
        'BACK': (-speed,-speed),
        'LEFT': (-speed,speed),
        'RIGHT': (speed,-speed)
    }
    
    return VELOCITY[direction]

def get_area(result):
    return result.ID, result.width * result.height

L,R = 0.0, 0.0
while True:
    if gp20.value == False:
        MOVE = not MOVE
        while gp20.value == False: # Wait until button is release
            pass
    
    results = hl.learnedBlocks() # Only get learned results
    
    if MOVE and results:
        r = results[0]
        #print(f"[{r.type}] (x:{r.x}, y:{r.y}), w:{r.width}, h:{r.height}")
        
        dist = euclideanDist((r.x,r.y))
        _, area = get_area(r)
        #print(f"Distance to center: {dist}")
        
        vThresh, vDirection = findVerticalPos((r.x,r.y))
        hThresh, hDirection = findHorizontalPos((r.x,r.y))
        
        if vThresh:
            L, R = getVelocity(vDirection, SPEED)
        else:
            if hThresh:
                L, R = getVelocity(hDirection, SPEED)
            else:
                L, R = 0, 0
                print('Stop')
    else:
        L,R=0,0
    
    print(L,R)
    Robot_Movement(L, R)
    time.sleep(0.1)
