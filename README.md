# CircuitPythonHuskyLens
HuskyLens SEN0305 using CircuitPython

# HUSKYLENS CircuitPython Library
09 JUN 2023

Credit:

(Python):

https://github.com/HuskyLens/HUSKYLENSPython
 
(MicroPython):

https://community.dfrobot.com/makelog-310469.html

<h3>Quick Start</h3>
<blockquote>
 <p>Place the <a href="/circuitPyHuskyLib.py">circuitPyHuskyLib.py</a> file within your projects folder</p>
 <p>You need to include this library in your CIRCUITPY/lib folder. You can download it from https://circuitpython.org/libraries</p>
 <ul><li>adafruit_bus_device</li></ul>
 <br>
 <p>UART</p>
 <code>import board</code><br>
 <code>from circuitPyHuskyLib import HuskyLensLibrary</code><br>
 <code>huskylens = HuskyLensLibrary("UART", TX=board.GP8, RX=board.GP9)</code><br>
 <code>print(huskylens.knock())</code><br>
 <br>
 <p>I2C</p>
 <code>import board</code><br>
 <code>from circuitPyHuskyLib import HuskyLensLibrary</code><br>
 <code>huskylens = HuskyLensLibrary("I2C", SCL=board.GP9, SDA=board.GP8)</code><br>
 <code>print(huskylens.knock())</code><br>
</blockquote>



