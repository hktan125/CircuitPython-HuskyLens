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
> You need to include this library in your **CIRCUITPY/lib** folder. 
> You can download it from https://circuitpython.org/libraries
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
 > **I2C**
 >```python
 >import board
 >from circuitPyHuskyLib import HuskyLensLibrary
 >huskylens = HuskyLensLibrary("I2C", SCL=board.GP9, SDA=board.GP8)
>
>print(huskylens.knock())
 >```

# Functions
#### Function Format Information
> **function_name(arg1, arg2, ...)**
> 
> Description:
> : Description of the inputs of the function and its functionality
> 
> Arguments:
> : arg1: (Type) Description
> : arg2: (Type) Description
>
> Return:
> : Description of the return value of the function, NONE if the function does not return. 


## General Functions
#### HuskyLensLibrary(proto, TX=None, RX=None, SCL=None, SDA=None, baudrate=9600, address=0x32, verbose=True)
>
>**Description:**  
>Create instance of the HuskyLens class. 
>
> **Attributes:**
> - SHAPE: (`tuple`) Constant value representing the shape/resolution of the HuskyLens (320, 240). 
>
>**Arguments:**
> - proto: (`str`) The protocol to be used ("UART" or "I2C")
> - TX: (`Pin`) The TX pin for UART communication (optional if I2C is used)
> - RX: (`Pin`) The RX pin for UART communication (optional if I2C is used)
> - SCL: (`Pin`) The SDA pin for I2C communication (optional if UART is used)
> - SDA: (`Pin`) The SCL pin for I2C communication (optional if UART is used)
> - baudrate: (`int`) The baudrate for UART communication (default: 9600)
> - address: (`int`) The I2C address of the HuskyLens (default: 0x32)
> - verbose: (`bool`) Whether to print "object not found" message (default: True)
>
>**Return:**  
>`HuskyLens` object
      
#### knock()
> **Description:**  
> Send a simple knock to the HuskyLens to ensure that you are connected and is able to communicate.
> 
> **Return:**  
> Return "Knock Received" on success

#### frameNumber()
> **Description:**  
> Get the number of frame HuskyLens have processed.
>
> **Return:**  
> Frame count

#### count()
> **Description:**  
> Get the number of detected objects on the screen.
> 
> **Return:**  
> Number of objects on screen. 

#### learnedObjCount()
> **Description:**  
> Get the total number of learned objects for the current running algorithm. 
> 
> **Return:**  
> Number of learned objects. 

## Data Functions
#### Data Format
- Data corresponds to either `block` information for all algorithms except *Line Tracking*, which instead will return `arrow` information. These directly reflect the blocks/arrows you see on the HuskyLens UI. 
> class Block:
> - x: (`int`) x coordinate of the center of the block.
> - y: (`int`) y coordinate of the center of the block.
> - x_topleft: (`int`) x coordinate of the top left corner of the block
> - y_topleft: (`int`) y coordinate of the top left corner of the block
> - width: (`int`) width of the block
> - height: (`int`) height of the block
> - ID: (`int`) object ID (if not learned, ID is 0)
> - learned: (`bool`) Is the object learned? (If object learned, learned is True)
> - type: (`str`) "BLOCK"
> 
> class Arrow:
> - xTail: (`int`) x coordinate of the tail of the arrow
> - yTail: (`int`) y coordinate of the tail of the arrow
> - xHead: (`int`) x coordinate of the head of the arrow
> - yHead: (`int`) x coordinate of the head of the arrow
> - ID: (`int`) object ID (if not learned, ID is 0)
> - learned: (`bool`) Is the object learned? (If object learned, learned is True)
> - type: (`str`) "ARROW"
> 
- Returned data will be in a list of either block or arrow information:  
Either `[block1, block2, ..., blockN]` or `[arrow1, arrow2, ..., arrowN]`

#### requestAll()
> **Description:**  
> Request all block or arrow data from HuskyLens. This will return **block/arrow** data for **all learned and unlearned** objects that are visible on the screen. 
>
> **Return:**  
> Data array either `[block1, block2, ..., blockN]` or `[arrow1, arrow2, ..., arrowN]`

#### blocks()
> **Description:**  
> Request all block data from HuskyLens. This will return **block** data for **all learned and unlearned** objects that are visible on the screen. 
> 
> **Return:**  
> Data array `[block1, block2, ..., blockN]`

#### arrows()
> **Description:**  
> Request all arrow data from HuskyLens. This will return **arrow** data for all **learned and unlearned** objects that are visible on the screen. 
> 
> **Return:**  
> Data array `[arrow1, arrow2, ..., arrowN]`

#### learned()
> **Description:**  
> Request all block or arrow data from HuskyLens . This will return **block/arrow data** for all **learned** objects that are visible on the screen, unlearned objects are ignored.
> 
> **Return:**  
> Data array either `[block1, block2, ..., blockN]` or `[arrow1, arrow2, ..., arrowN]`

#### learnedBlocks()
> **Description:**  
> Request all block data from HuskyLens. This will return **block** data for all **learned** objects that are visible on the screen, unlearned objects are ignored. 
> 
> **Return:**
> Data array `[block1, block2, ..., blockN]`

#### learnedArrows()
> **Description:**  
> Request all arrow data from HuskyLens. This will return **arrow** data for all **learned** objects that are visible on the screen, unlearned objects are ignored. 
> 
> **Return:**
> Data array `[arrow1, arrow2, ..., arrowN]`

#### getObjectByID(idVal)
> **Description:**  
> Request all **block or arrow** data from HuskyLens that have a designated **ID** and are visible on screen. 
> 
> **Arguments:**
> - idVal: (`int`) The desired ID of the object. 
> 
> **Return:**  
> Data array either `[block1, block2, ..., blockN]` or `[arrow1, arrow2, ..., arrowN]`

#### getBlocksByID(idVal)
> **Description:**  
> Request all **block** data from HuskyLens that have a designated **ID** and are visible on screen. 
> 
> **Arguments:**
> - idVal: (`int`) The desired ID of the object. 
> 
> **Return:**  
> Data array `[block1, block2, ..., blockN]`

#### getArrowsByID(idVal)
> **Description:**  
> Request all **arrow** data from HuskyLens that have a designated **ID** and are visible on screen. 
> 
> **Arguments:**
> - idVal: (`int`) The desired ID of the object. 
> 
> **Return:**  
> Data array `[arrow1, arrow2, ..., arrowN]`

## Algorithm Control Functions
#### algorithm(alg)
> **Description:**  
> Switch HuskyLens to a specific algorithm. 
> 
> **Arguments:**
> - alg: (`str`) The desired algorithm to switch to. 
>  ```python
>  "ALGORITHM_OBJECT_TRACKING"
> "ALGORITHM_FACE_RECOGNITION"
> "ALGORITHM_OBJECT_RECOGNITION"
> "ALGORITHM_LINE_TRACKING"
> "ALGORITHM_COLOR_RECOGNITION"
> "ALGORITHM_TAG_RECOGNITION"
> "ALGORITHM_OBJECT_CLASSIFICATION"
>  ```   
> 
> **Return:**
> "Knock Received" on success

#### learn(id)
> **Description:**  
> Learn the current recognized object on screen with a chosen ID
> 
> **Arguments:**
> - id: (`int`) The desired ID of the object (1 - 1023 range). 
> 
> **Return:**  
> "Knock Received" on success

#### forget()
> **Description:**  
> Forget learned objects for the current running algorithm. 
> 
> **Return:**  
> "Knock Received" on success

## UI Related Functions
#### setCustomName(name, id)
> **Description:**  
> Set a custom name for a learned object with a specified ID. 
> 
> **Arguments:**
> - name: (`str`) value for the desired name.  
> - id: (`int`) the object ID you wish to change.  
> 
> **Return:**  
> "Knock Received" on success

#### customText(name, x, y)
> **Description:**  
> - Place a string of text (less than 20 characters) on top of the HuskyLens UI. 
> - You can have at most 10 custom texts on the UI at once, and if you continue adding texts you will replace the previous texts in a circular fashion. 
> Each text is uniquely identified by its (x, y) coordinate, so you can replace the text string at a (x, y) coordinate instead of adding a new text object. 
> 
> **Arguments:**
> - name: (`str`) value for the desired text.  
> - x: (`int`) x coordinate of the top left corner of the text 
> - y: (`int`) y coordinate of the top left corner of the text
> 
> **Return:**  
> "Knock Received" on success

#### clearText()
> **Description:**  
> Clear and remove all custom UI texts from the screen. 
> 
> **Return:**  
> "Knock Received" on success

## Utility Functions
#### saveModelToSDCard(idVal)
> **Description:**  
> Save the current algorithms model file (its learned object data) to the SD Card. The file will be in this format: *AlgorithmName_Backup_idVal.conf*
> 
> **Arguments:**
> - idVal: (`int`) file number to be used in the name for the file.
> 
> **Return:**  
> "Knock Received" on success. If there is no SD Card inserted or SD Card error, there will be a UI popup on the HuskyLens. 

#### loadModelFromSDCard(idVal)
> **Description:**  
> Load a model file from the SD Card to the current algorithm and refresh the algorithm. The file will be in this format: *AlgorithmName_Backup_idVal.conf*
> 
> **Arguments:**
> - idVal: (`int`) file number to be used in the name for the file.
> 
> **Return:**  
> "Knock Received" on success. If there is no SD Card inserted or SD Card error, there will be a UI popup on the HuskyLens. 

#### savePictureToSDCard()
> **Description:**  
> Save a photo from the HuskyLens camera onto the SD Card. 
> 
> **Return:**  
> "Knock Received" on success. If there is no SD Card inserted or SD Card error, there will be a UI popup on the HuskyLens. 

#### saveScreenshotToSDCard()
> **Description:**  
> Save a screenshot of the HuskyLens UI onto the SD Card. 
> 
> **Return:**  
> "Knock Received" on success. If there is no SD Card inserted or SD Card error, there will be a UI popup on the HuskyLens. 
