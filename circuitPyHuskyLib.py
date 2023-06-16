# HUSKYLENS CircuitPython Library
# 09 JUN 2023
#
# Credit:
# Code base (reference) for Raspberry Pi:
# https://github.com/HuskyLens/HUSKYLENSPython
# 
# Code base (reference) for Raspberry Pi Pico (MicroPython):
# https://community.dfrobot.com/makelog-310469.html
#
# You need to include these libraries in your CIRCUITPY/lib folder. You can download it from https://circuitpython.org/libraries
# - adafruit_bus_device
#

# Example: 
'''
import board
from circuitPyHuskyLib import HuskyLensLibrary

# UART
huskylens = HuskyLensLibrary("UART", TX=board.GP8, RX=board.GP9)

# I2C
#huskylens = HuskyLensLibrary("I2C", SCL=board.GP9, SDA=board.GP8)

print(huskylens.knock())
'''

import binascii
import time
import busio
import adafruit_bus_device.i2c_device as i2c_device

commandHeaderAndAddress = "55AA11"
algorthimsByteID = {
    "ALGORITHM_OBJECT_TRACKING": "0100",
    "ALGORITHM_FACE_RECOGNITION": "0000",
    "ALGORITHM_OBJECT_RECOGNITION": "0200",
    "ALGORITHM_LINE_TRACKING": "0300",
    "ALGORITHM_COLOR_RECOGNITION": "0400",
    "ALGORITHM_TAG_RECOGNITION": "0500",
    "ALGORITHM_OBJECT_CLASSIFICATION": "0600",
}

class Arrow:
    def __init__(self, xTail, yTail , xHead , yHead, ID):
        self.xTail=xTail
        self.yTail=yTail
        self.xHead=xHead
        self.yHead=yHead
        self.ID=ID
        self.learned= True if ID > 0 else False
        self.type="ARROW"


class Block:
    def __init__(self, x, y , width , height, ID):
        self.x = x
        self.y=y
        self.width=width
        self.height=height
        self.ID=ID
        self.learned= True if ID > 0 else False
        self.type="BLOCK"

class HuskyLensLibrary:
    def __init__(self, proto, TX=None, RX=None, SCL=None, SDA=None, baudrate=9600, address=0x32):
        self.proto = proto
        self.address = address
        
        if (proto == "UART"):
            self.huskylensSer = busio.UART(TX, RX, baudrate=baudrate)
        elif (proto == "I2C"):
            i2c = busio.I2C(SCL, SDA)
            self.huskylensSer = i2c_device.I2CDevice(i2c, address)
        else:
            raise ValueError('Only support UART or I2C protocol')
        
        self.lastCmdSent = ""
        
    def writeToHuskyLens(self, cmd):
        self.lastCmdSent = cmd
        if (self.proto == "UART"):
            self.huskylensSer.write(cmd)
        else:
            with self.huskylensSer:
                self.huskylensSer.write(cmd)
        
    def calculateChecksum(self, hexStr):
        total = 0
        for i in range(0, len(hexStr), 2):
            total += int(hexStr[i:i+2], 16)
        hexStr = hex(total)[-2:]
        return hexStr
    
    def cmdToBytes(self, cmd):
        return binascii.unhexlify(cmd)
    
    def splitCommandToParts(self, str):
        headers = str[0:4]
        address = str[4:6]
        data_length = int(str[6:8], 16)
        command = str[8:10]
        if(data_length > 0):
            data = str[10:10+data_length*2]
        else:
            data = []
        checkSum = str[2*(6+data_length-1):2*(6+data_length-1)+2]

        return [headers, address, data_length, command, data, checkSum]
        
    def getBlockOrArrowCommand(self):
        byteString=b''
        if (self.proto == "UART"):
            byteString = self.huskylensSer.read(5)
            byteString += self.huskylensSer.read(int(byteString[3]))
            byteString += self.huskylensSer.read(1)
        else:
            byteString = bytearray(5)
            with self.huskylensSer:
                self.huskylensSer.readinto(byteString, start=0, end=5)
            byteString += bytearray(byteString[3]+1)
            with self.huskylensSer:
                self.huskylensSer.readinto(byteString, start=5, end=len(byteString))
        commandSplit = self.splitCommandToParts(''.join(['%02x' % b for b in byteString]))
        isBlock = True if commandSplit[3] == "2a" else False
        return (commandSplit[4], isBlock)
    
    def processReturnData(self, numIdLearnFlag=False, frameFlag=False):
        inProduction = True
        byteString=b''
        if (inProduction):
            try:
                if (self.proto == "UART"):
                    byteString = self.huskylensSer.read(5)
                    byteString += self.huskylensSer.read(int(byteString[3]))
                    byteString += self.huskylensSer.read(1)
                else:
                    byteString = bytearray(5)
                    with self.huskylensSer:
                        self.huskylensSer.readinto(byteString, start=0, end=5)
                    byteString += bytearray(byteString[3]+1)
                    with self.huskylensSer:
                        self.huskylensSer.readinto(byteString, start=5, end=len(byteString))
                
                # Convert byteString to hex first before splitCommandToParts
                commandSplit = self.splitCommandToParts(''.join(['%02x' % b for b in byteString]))
                if(commandSplit[3] == "2e"):
                    return "Knock Received"
                else:
                    returnData = []
                    numberOfBlocksOrArrow = int(
                        commandSplit[4][2:4]+commandSplit[4][0:2], 16)
                    numberOfIDLearned = int(
                        commandSplit[4][6:8]+commandSplit[4][4:6], 16)
                    frameNumber = int(
                        commandSplit[4][10:12]+commandSplit[4][8:10], 16)
                    
                    # Return empty list when no object is detected
                    if not (numberOfBlocksOrArrow):
                        print("No Object detected")
                        return []
                    
                    for i in range(numberOfBlocksOrArrow):
                        tmpObj = self.getBlockOrArrowCommand()
                        isBlock = tmpObj[1]
                        returnData.append(tmpObj[0])
                    finalData = []
                    tmp = []
                    for i in returnData:
                        tmp = []
                        for q in range(0, len(i), 4):
                            low = int(i[q:q+2], 16)
                            high = int(i[q+2:q+4], 16)
                            if (high > 0):
                                val = low + 255 + high
                            else:
                                val = low
                            tmp.append(val)
                        finalData.append(tmp)
                    ret = self.convert_to_class_object(finalData, isBlock)
                    if(numIdLearnFlag):
                        ret.append(numberOfIDLearned)
                    if(frameFlag):
                        ret.append(frameNumber)
                    return ret
            except:
                print("Read response error, please try again")
                return []
    
    def convert_to_class_object(self,data,isBlock):
        tmp=[]
        for i in data:
            if(isBlock):
                obj = Block(i[0],i[1],i[2],i[3],i[4])
            else:
                obj = Arrow(i[0],i[1],i[2],i[3],i[4])
            tmp.append(obj)
        return tmp
    
    def algorithm(self, alg):
        if alg in algorthimsByteID:
            cmd = commandHeaderAndAddress+"022d"+algorthimsByteID[alg]
            cmd += self.calculateChecksum(cmd)
            cmd = self.cmdToBytes(cmd)
            self.writeToHuskyLens(cmd)
            return self.processReturnData()
        else:
            print("INCORRECT ALGORITHIM NAME")

    def arrows(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002232")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
    
    def blocks(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002131")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
    
    def clearText(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"003545")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
    
    def count(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002030")
        self.writeToHuskyLens(cmd)
        return len(self.processReturnData())
    
    def frameNumber(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002030")
        self.writeToHuskyLens(cmd)
        return self.processReturnData(frameFlag=True)[-1]
    
    def forget(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"003747")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
    
    def knock(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002c3c")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
    
    def learned(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002333")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
    
    def learnedArrows(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002535")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
    
    def learnedBlocks(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002434")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
    
    def learnedObjCount(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002030")
        self.writeToHuskyLens(cmd)
        return self.processReturnData(numIdLearnFlag=True)[-1]
    
    def requestAll(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002030")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
    
    def savePictureToSDCard(self):
        self.huskylensSer.timeout=5
        cmd = self.cmdToBytes(commandHeaderAndAddress+"003040")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
    
    def saveScreenshotToSDCard(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"003949")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
    
    def getObjectByID(self, idVal):
        idVal = "{:04x}".format(idVal)
        idVal = idVal[2:]+idVal[0:2]
        cmd = commandHeaderAndAddress+"0226"+idVal
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def getBlocksByID(self, idVal):
        idVal = "{:04x}".format(idVal)
        idVal = idVal[2:]+idVal[0:2]
        cmd = commandHeaderAndAddress+"0227"+idVal
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def getArrowsByID(self, idVal):
        idVal = "{:04x}".format(idVal)
        idVal = idVal[2:]+idVal[0:2]
        cmd = commandHeaderAndAddress+"0228"+idVal
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def learn(self, id):
        cmd = commandHeaderAndAddress
        data = "{:04x}".format(id)
        part1=data[2:]
        part2=data[0:2]
        #reverse to correct endiness
        data=part1+part2
        cmd += "{:02x}".format(len(data)//2)
        cmd += "{:02x}".format(0x36)
        cmd += data
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
    
    def setCustomName(self, name, id):
        localId = "{:02x}".format(id)
        nameDataSize = "{:02x}".format(len(name)+1)
        name_ = ""
        for char in name:
            name_ += "{:02x}".format(ord(char))
        name_ += "{:02x}".format(0)
        data = localId+nameDataSize+name_
        dataLength = len(data)//2
        cmd = commandHeaderAndAddress
        cmd += "{:02x}".format(dataLength)
        cmd += "{:02x}".format(0x2f)
        cmd += data
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
    
    def customText(self, name, x, y):
        name_=""
        for char in name:
            name_ += "{:02x}".format(ord(char))
            
        nameDataSize = "{:02x}".format(len(name))
        
        if (x > 255):
            x = "ff"+"{:02x}".format(x%255)
        else:
            x = "00"+"{:02x}".format(x)
        y = "{:02x}".format(y)
            
        data = nameDataSize + x + y + name_
        dataLength = "{:02x}".format(len(data)//2)
        
        cmd = commandHeaderAndAddress
        cmd += dataLength
        cmd += "{:02x}".format(0x34)
        cmd += data
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()
    
    def saveModelToSDCard(self,idVal):
        idVal = "{:04x}".format(idVal)
        idVal = idVal[2:]+idVal[0:2]
        cmd = commandHeaderAndAddress+"0232"+idVal
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def loadModelFromSDCard(self,idVal):
        idVal = "{:04x}".format(idVal)
        idVal = idVal[2:]+idVal[0:2]
        cmd = commandHeaderAndAddress+"0233"+idVal
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

