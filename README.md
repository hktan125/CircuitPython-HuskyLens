# CircuitPython-HuskyLens
HuskyLens SEN0305 using CircuitPython

# HUSKYLENS CircuitPython Library
09 JUN 2023

Credit:
HuskyLens (Python):
https://github.com/HuskyLens/HUSKYLENSPython

RRoy from DFRobot community (MicroPython):
https://community.dfrobot.com/makelog-310469.html

### Quick Start
> Place the [circuitPyHuskyLib.py](/circuitPyHuskyLib.py) file within your projects folder. 
>
> You need to include this library in your **CIRCUITPY/lib** folder. You can download it from https://circuitpython.org/libraries
> - adafruit_bus_device
> 
> **UART**
> ```python
> import board
> from circuitPyHuskyLib import HuskyLensLibrary
> huskylens = HuskyLensLibrary("UART", TX=board.GP8, RX=board.GP9)
> 
> print(huskylens.knock())
> ```
 >
 >**I2C**
 >```python
 >import board
 >from circuitPyHuskyLib import HuskyLensLibrary
 >huskylens = HuskyLensLibrary("I2C", SCL=board.GP9, SDA=board.GP8)
>
>print(huskylens.knock())
 >```
