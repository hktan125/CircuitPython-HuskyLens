# line_tracking_robot_v2.py
import time
import board
import digitalio
import pwmio
from math import sqrt, acos, degrees
from adafruit_motor import motor

from circuitPyHuskyLib import HuskyLensLibrary

hl = HuskyLensLibrary('UART', TX=board.GP12, RX=board.GP13)
hl.algorithm("ALGORITHM_LINE_TRACKING") # Redirect to Line Tracking Function
hl.clearText()

# Init value
MOVE = True
L, R = 0, 0
ANGLE_THRESHOLD = 89
INIT_SPEED = 0.3

VELOCITY = {
    'FRONT': (INIT_SPEED,INIT_SPEED),
    'BACK': (-INIT_SPEED,-INIT_SPEED),
    'LEFT': (-INIT_SPEED,INIT_SPEED),
    'RIGHT': (INIT_SPEED,-INIT_SPEED),
    'END_LINE': (0,0),
}

# Check
assert ANGLE_THRESHOLD < 90, "Angle need to be less than 90"

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

def find_line_midpoint(cor1, cor2):
    x1, y1 = cor1
    x2, y2 = cor2
    return (x1+x2)/2, (y1+y2)/2

def euclideanDist(p1, p2):
    x1,y1 = p1
    x2,y2 = p2
    return sqrt((x1-x2)**2+(y1-y2)**2)

def calibration(p1, p2):
    # Calibrate if the midpoint of the line is not in region as shown in the draft
    xmid, ymid = find_line_midpoint(p1, p2)
    
    if (xmid > 80 and xmid <= 240 and ymid > 60 and ymid <= 180):
        return None
    
    if (p1[1] > 120):
        return "END_LINE"
    
    if (ymid > 0 and ymid <= 60):
        return "FRONT"
    
    if (ymid > 180 and ymid <= 240):
        return "BACK"
    
    if (xmid > 0 and xmid <= 80):
        return "LEFT"
    
    if (xmid > 240 and xmid <= 320):
        return "RIGHT"
    

def findPosition(p1, p2):
    # Head (x1,y1)
    # Tail (x2,y2)
    # Head - Tail < 0, (False) ==> Left
    # Head - Tail > 0, (True) ==> Right
    x1,y1 = p1
    x2,y2 = p2
    
    x = x2-x1
    
    return True if x>0 else False

def findAngle(p1, p2):
    xmid, ymid = find_line_midpoint(p1, p2)
    x1, y1 = p1
    
    # adjacent
    a_dist = euclideanDist((xmid, ymid), (xmid, y1))
    # hypotenuse
    h_dist = euclideanDist((xmid, ymid), (x1, y1))
    # opposite
    o_dist = euclideanDist((x1, y1),(xmid,y1))
    
    #print(h_dist, a_dist, o_dist)
    
    # Horizontal line causing ZeroDivisionError
    if a_dist <= 0:
        a_dist = 1 # 1 * (any number) = 1
    
    # https://en.wikipedia.org/wiki/Law_of_cosines
    return degrees(acos((a_dist * a_dist + h_dist * h_dist - o_dist * o_dist)/(2.0 * a_dist * h_dist)))

def deg_to_speed(deg, turn, maxSpeed=INIT_SPEED):
    if deg > ANGLE_THRESHOLD: # Stop moving
        # (-)INIT_SPEED because we will add INIT_SPEED later
        # -0.3 + 0.3 = 0
        return -INIT_SPEED, -INIT_SPEED
    
    speed = (deg/ANGLE_THRESHOLD) * maxSpeed
    
    # turn = False = Left
    # turn = True = Right
    if turn:
        return -abs(speed), speed
    else:
        return speed, -abs(speed)

def Robot_Movement(sL, sR):
    motorL.throttle = sL
    motorR.throttle = sR

while True:
    if gp20.value == False:
        MOVE = not MOVE
        while gp20.value == False: # Wait until button is release
            pass
    
    results = hl.learnedArrows() # Get learned line
    
    if MOVE and results:
        r = results[0]
        print(f"[{r.type}] Head:(x:{r.xHead}, y:{r.yHead}), Tail:(x:{r.xTail}, y:{r.yTail})")
        
        direction = calibration((r.xHead, r.yHead),(r.xTail, r.yTail))
        
        if direction:
            L, R = VELOCITY[direction]
            print('Recalibrate')
        else:
            turn = findPosition((r.xHead, r.yHead),(r.xTail, r.yTail))
            angle = findAngle((r.xHead, r.yHead),(r.xTail, r.yTail))
            L, R = deg_to_speed(angle, turn)
            print(f'TURN: {turn}, DEG: {angle}, SPEED: {L},{R}')
            
            L += INIT_SPEED
            R += INIT_SPEED
        
    else:
        L,R = 0, 0
    
    print(L,R)
    Robot_Movement(L,R)
    #L,R = 0,0 # Reset
    time.sleep(0.1)
