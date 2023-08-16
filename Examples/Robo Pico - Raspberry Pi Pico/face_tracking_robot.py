# face_tracking_robot.py

import time
import board
import digitalio
import pwmio
from math import sqrt
from adafruit_motor import motor

from circuitPyHuskyLib import HuskyLensLibrary

DIST_THRESHOLD = 20
AREA_NEAR_THRESHOLD = 9000
AREA_FAR_THRESHOLD = 3500

hl = HuskyLensLibrary('UART', TX=board.GP12, RX=board.GP13)
hl.algorithm("ALGORITHM_FACE_RECOGNITION") # Redirect to face Function
hl.clearText()

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

gp21 = digitalio.DigitalInOut(board.GP21)
gp21.direction = digitalio.Direction.INPUT

MOVE = True
RECOGNITION = False

def show_text(movement, mode):
    hl.algorithm("ALGORITHM_FACE_RECOGNITION") # Redirect to face Function
    if movement:
        hl.customText('ON', 280, 20)
    else:
        hl.customText('OFF', 270, 20)
    
    if mode:
        hl.customText('Recognition mode',20,20)
        hl.customText('GP21 to change mode',20,50)
    else:
        hl.customText('Detection mode',20,20)
        hl.customText('GP21 to change mode',20,50)

def Robot_Movement(sL, sR):
    motorL.throttle = sL
    motorR.throttle = sR

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
    # x2 - x1 > 0, (positive/True) ==> [object position is less than center]
    # x2 - x1 < 0, (negative/False) ==> [object position is more than center]
    x1,y1 = p1
    x2,y2 = p2
    
    x = x2-x1
    y = y2-y1
    
    return True if x>0 else False, True if y>0 else False

def get_area(result):
    return result.ID, result.width * result.height

def get_max_area(list_of_id_area):
    # Sort the list_of_id_area based on the ID
    sorted_list = sorted(list_of_id_area, key=lambda x: x[0])

    # Create a dictionary to store the grouped data
    grouped_data = {}

    # Iterate over the sorted list and group the data by the ID
    for item in sorted_list:
        id = item[0]
        area = item[1]
        
        if id not in grouped_data:
            grouped_data[id] = []
        
        grouped_data[id].append(area)

    # Find the maximum area and corresponding ID
    max_area = 0
    max_id = None

    for id, areas in grouped_data.items():
        max_area_in_group = max(areas)
        
        if max_area_in_group > max_area:
            max_area = max_area_in_group
            max_id = id
    
    
    idx = list_of_id_area.index((max_id, max_area))
    
    # Print the maximum area and corresponding ID(in huskylens), and idx(index in list)
    return max_id, max_area, idx

show_text(MOVE, RECOGNITION)
L,R = 0.0, 0.0
while True:
    if gp20.value == False:
        MOVE = not MOVE
        hl.clearText()
        show_text(MOVE, RECOGNITION)
        while gp20.value == False: # Wait until button is release
            pass
    
    if gp21.value == False:
        RECOGNITION = not RECOGNITION
        hl.clearText()
        show_text(MOVE, RECOGNITION)
        while gp21.value == False: # Wait until button is release
            pass
    
    if RECOGNITION:
        results = hl.learnedBlocks() # Only get learned results
    else:
        results = hl.blocks()
    
    if MOVE and results:
        area_list = list(map(get_area, results)) # Calculate area for each result
        print(area_list)
        max_id, max_area, idx_max = get_max_area(area_list)
        r = results[idx_max]
        #print(f"[{r.type}] (x:{r.x}, y:{r.y}), w:{r.width}, h:{r.height}")
        
        dist = euclideanDist((r.x,r.y))
        _, area = get_area(r)
        #print(f"Distance to center: {dist}")
        
        if dist > DIST_THRESHOLD:
            xRelPos = findPosition((r.x, r.y))[0]
            
            if xRelPos:
                L = -0.2
                R = 0.2
                print('Turn left')
            else:
                L = 0.2
                R = -0.2
                print('Turn right')
        else:
            L = 0
            R = 0
            print('stop turn')
            
        if area > AREA_NEAR_THRESHOLD:
            L += -0.3
            R += -0.3
        elif area < AREA_FAR_THRESHOLD:
            L += 0.3
            R += 0.3
        
        print(area)
    else:
        L,R=0,0
    
    print(L,R)
    Robot_Movement(L, R)
    L,R = 0,0 # Reset
    time.sleep(0.1)
