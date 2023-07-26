# oled_prs_game.py
# Paper Rock Scissor game with Object classification
'''
GP20 - Start game
GP22 - Settings

'''

import board
import busio
import time
import random
import digitalio
import adafruit_ssd1306
from circuitPyHuskyLib import HuskyLensLibrary

hl = HuskyLensLibrary('UART', TX=board.GP8, RX=board.GP9)

i2c = busio.I2C(board.GP1, board.GP0)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
#oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

# Buttons (GP20,21,22)
gp20 = digitalio.DigitalInOut(board.GP20)
gp20.direction = digitalio.Direction.INPUT
gp21 = digitalio.DigitalInOut(board.GP21)
gp21.direction = digitalio.Direction.INPUT
gp22 = digitalio.DigitalInOut(board.GP22)
gp22.direction = digitalio.Direction.INPUT

name = {1: "Paper",
        2: "Rock",
        3: "Scissors",
        4: "??"}

# Choices of name id
selection = [1, 2, 3]

# Clear screen
oled.fill(0)
oled.show()

PLAY = False
LEARN_FORGET = False

xpos = 0
PAGE = 0 # Store page count for settings
GAME = 0 # Store game count
USER = 0 # Store score for user
COMPUTER = 0 # Store score for computer

def countdown():
    oled.fill(0)
    oled.text("3", 128//2, 64//3, 1, size=3)
    oled.show()
    time.sleep(1)
    oled.fill(0)
    oled.text("2", 128//2, 64//3, 1, size=3)
    oled.show()
    time.sleep(1)
    oled.fill(0)
    oled.text("1", 128//2, 64//3, 1, size=3)
    oled.show()
    time.sleep(1)

def getWinner(c1, c2):
    if c1 == c2:
        return 0, 0
    
    if c1 == 1:
        if c2 == 2:
            return 1, 0
        else:
            return 0, 1
    
    if c1 == 2:
        if c2 == 3:
            return 1, 0
        else:
            return 0, 1
    
    if c1 == 3:
        if c2 == 1:
            return 1, 0
        else:
            return 0, 1
        
    if c1 > 3:
        return 0, 1
    elif c2 > 3:
        return 1, 0

def getFinalWinner(u, c): # Compare score
    if u == c:
        return None
    
    if u > c:
        return "User"
    else:
        return "Computer"

hl.algorithm("ALGORITHM_OBJECT_CLASSIFICATION") # Redirect to Object Classification Function
while True:
    if not PLAY:
        if gp20.value == False:
            PLAY = True
            while gp20.value == False:
                pass
        elif gp22.value == False:
            xpos = 0
            if PAGE >= 3:
                PAGE = 0
            else:
                PAGE += 1
            while gp22.value == False:
                pass
    
    if PAGE == 1:
        xpos = 0
        oled.fill(0)
        oled.text(
            f'''Settings {PAGE}\n\nGP20 - Paper\n\nGP21 - Rock\n\nGP22 - Next Page''', 5, 5, 1)
        oled.show()
        if gp20.value == False: # Paper
            while gp20.value == False:
                hl.learn(1)
        elif gp21.value == False: # Rock
            while gp21.value == False:
                hl.learn(2)
        continue
    elif PAGE == 2:
        xpos = 0
        oled.fill(0)
        oled.text(
            f'''Settings {PAGE}\n\nGP20 - Scissors\n\nGP21 - Environment\n\nGP22 - Next Page''', 5, 5, 1)
        oled.show()
        if gp20.value == False: # Scissors
            while gp20.value == False:
                hl.learn(3)
        elif gp21.value == False: # Environment
            while gp21.value == False:
                hl.learn(4)
        continue
    elif PAGE == 3:
        xpos = 0
        oled.fill(0)
        oled.text(
            f'''Settings {PAGE}\n\nGP20 - Forget\n\nGP22 - Exit Settings''', 5, 5, 1)
        oled.show()
        if gp20.value == False: # Forget
            hl.forget()
            while gp20.value == False:
                pass
        continue
    elif PAGE == 0:
        if GAME >= 5:
            winner = getFinalWinner(USER, COMPUTER)
            print(f'{winner} wins' if winner != None else 'Draw')
            oled.fill(0)
            oled.text(f'{winner}\nwins' if winner != None else 'Draw', 5, 30, 1, size=2)
            oled.show()
            
            GAME = 0
            USER = 0
            COMPUTER = 0
            PLAY = False
            time.sleep(3)
        elif PLAY:
            check_learned = hl.learnedBlocks()
            if not check_learned:
                PLAY = False
                oled.fill(0)
                oled.text("HuskyLens haven't\nlearn yet", 5,5, 1)
                oled.show()
                time.sleep(2)
                continue
            
            countdown()
            GAME += 1
            
            choice = random.choice(selection)
            
            results = hl.learnedBlocks() # Only get learned results
            
            if results: # if result not empty
                r = results[0]
                
                u, c = getWinner(r.ID, choice)
                USER += u
                COMPUTER += c
                oled.fill(0)
                print(f"ID: {r.ID}, {name[r.ID] if r.ID <= 4 else name[4]} ==== ID: {choice}, {name[choice]} [{USER} - {COMPUTER}]")
                oled.text("User", 5, 5, 1)
                oled.text(f"{name[r.ID] if r.ID <= 4 else name[4]}", 5, 15, 1, size=2)
                oled.text(f"{USER}", 128-20, 15, 1, size=2)
                oled.hline(0, 35, 128, 1)
                oled.text("Computer", 5, 40, 1)
                oled.text(f"{name[choice]}", 5, 50, 1, size=2)
                oled.text(f"{COMPUTER}", 128-20, 50, 1, size=2)
                oled.show()
                time.sleep(1)
        else:
            if xpos > 128:
                xpos = -128
            
            oled.fill(0)
            oled.text('GP20 - Start', xpos, 20, 1, size=2)
            xpos += 5
            oled.show()
            continue
