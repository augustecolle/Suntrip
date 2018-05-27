import serial as serial
import time
import binascii
import numpy as np

DevNode = "01" #device node, manual configured on machine, standard value is 01
pause = 0.01 #used for a timeout between sending command and reading buffer for the response
vNom = 80.0 #on machine, nominal votage
iNom = 200.0
pNom = 2400.0
rNom = 100


def startSerial(port = '/dev/ttyUSB0', devicenode = "02"):
    '''Initialize serial communication with the default values on page 28 of the programming manual. The devicenode (global DevNode, a two character string) is standard set to "01" but is device dependent, the port is standard set to /dev/ttyUSB0 cause this program was written on a linux distribution'''
    global DevNode
    global ser
    DevNode = devicenode
    ser = serial.Serial(port, baudrate=57600, parity=serial.PARITY_ODD, stopbits=serial.STOPBITS_ONE, timeout=0)
    return ser


def stopSerial():
    '''Stops serial communication'''
    global ser
    ser.close()
    return 0


def clearBuffer():
    ser.flushInput()
    ser.flushOutput()


def checksum(dataList):
    '''calculates checksum and returns it'''
    checksum = 0
    for hexVal in dataList:
        checksum += int(binascii.hexlify(hexVal).decode('UTF-8'), 16)
    checksum = hex(checksum)[2:].zfill(4)
    return bytes.fromhex(checksum)


def readAndTreat(maxbytes = 20):
    '''Reads and treats the incomming data. The default value for the maximum on incomming bytes is arbitrary set to 100, although not so arbitrary since I think a larger response from the device is not possible unless one forgets to read the buffer. Returns the treated data as an array of hex numbers'''
    time.sleep(0.05)
    inBuffer = ser.read(maxbytes)
    inBuffer = binascii.hexlify(inBuffer).decode('UTF-8')
    inBuffer = [inBuffer[i:i+2] for i in range(0, len(inBuffer), 2)]
    return inBuffer


def setCurrentA(current):
    '''set current, expects float value in Ampere. There is an offset of 0.1A which is corrected in tthis function'''
    global DevNode
    global iNom
    global pause
    offset = 0.1 #measured offset with fluke 80i-110s

    SD = b'\xD1'
    DN = bytes.fromhex(DevNode)
    OBJ = b'\x33'
    setValue = hex(int(np.round((offset + current)*25600.0/iNom))).replace("0x","").zfill(4)
    print(setValue)
    DATA1 = bytes.fromhex(setValue[:2])
    DATA2 = bytes.fromhex(setValue[2:])
    CS = checksum([SD, DN, OBJ, DATA1, DATA2])
    get_query = SD+DN+OBJ+DATA1+DATA2+CS
    ser.write(get_query)
    return 0;


def setPowerA(power):
    '''set power, expects float value in Watts. Power accuracy of < 2% so I implemented a feedback loop to establish a more accurate voltage setting based on the difference between measured and setted value'''
    global DevNode
    global pNom
    global pause
    correctedPower = power

    for x in range(20):
        SD = b'\xD1'
        DN = bytes.fromhex(DevNode)
        OBJ = b'\x34'
        setValue = hex(int(np.round(correctedPower*25600.0/pNom))).replace("0x","").zfill(4)
        print(setValue)
        DATA1 = bytes.fromhex(setValue[:2])
        DATA2 = bytes.fromhex(setValue[2:])
        CS = checksum([SD, DN, OBJ, DATA1, DATA2])
        get_query = SD+DN+OBJ+DATA1+DATA2+CS
        ser.write(get_query)
        correctedPower = getPowerA() + 0.08*(power - getActualValues()[2])
    return 0;


def setCCMode():
    global DevNode
    global pause

    SD = b'\xD1'
    DN = bytes.fromhex(DevNode)
    OBJ = b'\x36'
    setValue = hex(0x0E00).replace("0x","").zfill(4)
    DATA1 = bytes.fromhex(setValue[:2])
    DATA2 = bytes.fromhex(setValue[2:])
    CS = checksum([SD, DN, OBJ, DATA1, DATA2])
    get_query = SD+DN+OBJ+DATA1+DATA2+CS
    ser.write(get_query)
    return 0;


def setCVMode():
    global DevNode
    global pause

    SD = b'\xD1'
    DN = bytes.fromhex(DevNode)
    OBJ = b'\x36'
    setValue = hex(0x0E02).replace("0x","").zfill(4)
    DATA1 = bytes.fromhex(setValue[:2])
    DATA2 = bytes.fromhex(setValue[2:])
    CS = checksum([SD, DN, OBJ, DATA1, DATA2])
    get_query = SD+DN+OBJ+DATA1+DATA2+CS
    ser.write(get_query)
    return 0;


def setCPMode():
    global DevNode
    global pause

    SD = b'\xD1'
    DN = bytes.fromhex(DevNode)
    OBJ = b'\x36'
    setValue = hex(0x0E04).replace("0x","").zfill(4)
    DATA1 = bytes.fromhex(setValue[:2])
    DATA2 = bytes.fromhex(setValue[2:])
    CS = checksum([SD, DN, OBJ, DATA1, DATA2])
    get_query = SD+DN+OBJ+DATA1+DATA2+CS
    ser.write(get_query)
    return 0;


def setCR1Mode():
    global DevNode
    global pause

    SD = b'\xD1'
    DN = bytes.fromhex(DevNode)
    OBJ = b'\x36'
    setValue = hex(0x0E6).replace("0x","").zfill(4)
    DATA1 = bytes.fromhex(setValue[:2])
    DATA2 = bytes.fromhex(setValue[2:])
    CS = checksum([SD, DN, OBJ, DATA1, DATA2])
    get_query = SD+DN+OBJ+DATA1+DATA2+CS
    ser.write(get_query)
    return 0;


def setCR2Mode():
    global DevNode
    global pause

    SD = b'\xD1'
    DN = bytes.fromhex(DevNode)
    OBJ = b'\x36'
    setValue = hex(0x0E08).replace("0x","").zfill(4)
    DATA1 = bytes.fromhex(setValue[:2])
    DATA2 = bytes.fromhex(setValue[2:])
    CS = checksum([SD, DN, OBJ, DATA1, DATA2])
    get_query = SD+DN+OBJ+DATA1+DATA2+CS
    ser.write(get_query)
    return 0;

def setRemoteControllOn():
    '''set load controll, bit 0 for switching input (1 = on), bit 3-1 regulation mode (000 = CC, 001 = CV, 010 = CP, 011 = CR1, 100 = CR2), bit 4 set remote (1 = remote controll), bit 6-5 control mode (00 = level A, 01 = Battery, 10 = level A/B, 11 = level B). Two byte register but one byte data'''
    global DevNode
    global pause

    SD = b'\xD1'
    DN = bytes.fromhex(DevNode)
    OBJ = b'\x36'
    setValue = hex(0x1010).replace("0x","").zfill(4)
    DATA1 = bytes.fromhex(setValue[:2])
    DATA2 = bytes.fromhex(setValue[2:])
    CS = checksum([SD, DN, OBJ, DATA1, DATA2])
    get_query = SD+DN+OBJ+DATA1+DATA2+CS
    ser.write(get_query)
    return 0;

def setRemoteControllOff():
    '''set load controll, bit 0 for switching input (1 = on), bit 3-1 regulation mode (000 = CC, 001 = CV, 010 = CP, 011 = CR1, 100 = CR2), bit 4 set remote (1 = remote controll), bit 6-5 control mode (00 = level A, 01 = Battery, 10 = level A/B, 11 = level B). Two byte register but one byte data'''
    global DevNode
    global vNom
    global pause

    SD = b'\xD1'
    DN = bytes.fromhex(DevNode)
    OBJ = b'\x36'
    setValue = hex(0x1000).replace("0x","").zfill(4)
    DATA1 = bytes.fromhex(setValue[:2])
    DATA2 = bytes.fromhex(setValue[2:])
    CS = checksum([SD, DN, OBJ, DATA1, DATA2])
    get_query = SD+DN+OBJ+DATA1+DATA2+CS
    ser.write(get_query)
    return 0;


def setInputOn():
    '''set load controll, bit 0 for switching input (1 = on), bit 3-1 regulation mode (000 = CC, 001 = CV, 010 = CP, 011 = CR1, 100 = CR2), bit 4 set remote (1 = remote controll), bit 6-5 control mode (00 = level A, 01 = Battery, 10 = level A/B, 11 = level B). Two byte register but one byte data'''
    global DevNode
    global vNom
    global pause

    SD = b'\xD1'
    DN = bytes.fromhex(DevNode)
    OBJ = b'\x36'
    setValue = hex(0x0101).replace("0x","").zfill(4)
    DATA1 = bytes.fromhex(setValue[:2])
    DATA2 = bytes.fromhex(setValue[2:])
    CS = checksum([SD, DN, OBJ, DATA1, DATA2])
    get_query = SD+DN+OBJ+DATA1+DATA2+CS
    ser.write(get_query)
    return 0;


def setInputOff():
    '''set load controll, bit 0 for switching input (1 = on), bit 3-1 regulation mode (000 = CC, 001 = CV, 010 = CP, 011 = CR1, 100 = CR2), bit 4 set remote (1 = remote controll), bit 6-5 control mode (00 = level A, 01 = Battery, 10 = level A/B, 11 = level B). Two byte register but one byte data'''
    global DevNode
    global vNom
    global pause

    SD = b'\xD1'
    DN = bytes.fromhex(DevNode)
    OBJ = b'\x36'
    setValue = hex(0x0100).replace("0x","").zfill(4)
    DATA1 = bytes.fromhex(setValue[:2])
    DATA2 = bytes.fromhex(setValue[2:])
    CS = checksum([SD, DN, OBJ, DATA1, DATA2])
    get_query = SD+DN+OBJ+DATA1+DATA2+CS
    ser.write(get_query)
    return 0;


def getCurrentA():
    '''gets set value for current channel A'''
    global iNom

    SD = b'\x51'
    DN = bytes.fromhex(DevNode)
    OBJ = b'\x33'
    CS = checksum([SD, DN, OBJ])
    get_query = SD+DN+OBJ+CS
    ser.write(get_query)
    treatedData = readAndTreat()
    current = int((treatedData[3]+treatedData[4]).replace("0x",""), 16)*iNom/25600.0
    return current;


def getPowerA():
    '''gets set value for power channel A'''
    global pNom

    SD = b'\x51'
    DN = bytes.fromhex(DevNode)
    OBJ = b'\x34'
    CS = checksum([SD, DN, OBJ])
    get_query = SD+DN+OBJ+CS
    ser.write(get_query)
    treatedData = readAndTreat()
    power = int((treatedData[3]+treatedData[4]).replace("0x",""), 16)*pNom/25600.0
    return power;


def getVoltageA():
    '''gets set value for voltage channel A'''
    global vNom

    SD = b'\x51'
    DN = bytes.fromhex(DevNode)
    OBJ = b'\x32'
    CS = checksum([SD, DN, OBJ])
    get_query = SD+DN+OBJ+CS
    ser.write(get_query)
    treatedData = readAndTreat()
    voltage = int((treatedData[3]+treatedData[4]).replace("0x",""), 16)*vNom/25600.0
    return voltage;


def getDeviceState():
    '''get device state'''
    global DevNode
    global vNom
    global pause
    SD = b'\x51'
    DN = bytes.fromhex(DevNode)
    OBJ = b'\x46'
    CS = checksum([SD, DN, OBJ])
    get_query = SD+DN+OBJ+CS
    ser.write(get_query)
    time.sleep(pause)
    treatedData = readAndTreat()
    time.sleep(pause)
    clearBuffer()
    return treatedData;


def getLoadControl():
    '''get load control'''
    global DevNode
    global pause

    SD = b'\x51'
    DN = bytes.fromhex(DevNode)
    OBJ = b'\x36'
    #no data object in querying, see manual page 28
    CS = checksum([SD, DN, OBJ])
    get_query = SD+DN+OBJ+CS
    time.sleep(0.005)
    ser.write(get_query)
    treatedData = readAndTreat()
    return treatedData


def getNominalVoltage():
    global DevNode
    global pause

    SD = b'\x53'
    DN = bytes.fromhex(DevNode)
    OBJ = b'\x02'
    CS = checksum([SD, DN, OBJ])
    get_query = SD+DN+OBJ+CS
    ser.write(get_query)
    treatedData = readAndTreat()
    voltage = int2flp(int((treatedData[3]+treatedData[4]+treatedData[5]+treatedData[6]).replace("0x",""), 16))
    return voltage;


def getNominalPower():
    global DevNode
    global pause

    SD = b'\x53'
    DN = bytes.fromhex(DevNode)
    OBJ = b'\x04'
    CS = checksum([SD, DN, OBJ])
    get_query = SD+DN+OBJ+CS
    ser.write(get_query)
    treatedData = readAndTreat()
    power = int2flp(int((treatedData[3]+treatedData[4]+treatedData[5]+treatedData[6]).replace("0x",""), 16))
    return power;


def getActualValues():
    '''get voltage, current and power. These are read only'''
    global DevNode
    global vNom
    global iNom
    global pNom
    global pause

    SD = b'\x55'
    DN = bytes.fromhex(DevNode)
    OBJ = b'\x47'
    #no data object in querying, see manual page 28
    CS = checksum([SD, DN, OBJ])
    get_query = SD+DN+OBJ+CS
    time.sleep(0.05)
    ser.write(get_query)
    treatedData = readAndTreat()
    voltage = int((treatedData[3]+treatedData[4]).replace("0x",""), 16)*vNom/25600.0
    current = int((treatedData[5]+treatedData[6]).replace("0x",""), 16)*iNom/25600.0
    power = int((treatedData[7]+treatedData[8]).replace("0x",""), 16)*pNom/25600.0
    return [voltage, current, power]


def getSoftwareVersion():
    '''get software version number'''
    global DevNode
    global pause

    SD = b'\x5F'
    DN = bytes.fromhex(DevNode)
    OBJ = b'\x09'
    #no data object in querying, see manual page 28
    CS = checksum([SD, DN, OBJ])
    get_query = SD+DN+OBJ+CS
    time.sleep(0.005)
    ser.write(get_query)
    treatedData = readAndTreat()
    test = [chr(int(treatedData[x], 16)) for x in range(len(treatedData))]
    return test


def getFirmwareVersion():
    '''get firmware version number'''
    global DevNode
    global pause

    SD = b'\x56'
    DN = bytes.fromhex(DevNode)
    OBJ = b'\x0D'
    #no data object in querying, see manual page 28
    CS = checksum([SD, DN, OBJ])
    get_query = SD+DN+OBJ+CS
    time.sleep(0.005)
    ser.write(get_query)
    treatedData = readAndTreat()
    test = [chr(int(treatedData[x], 16)) for x in range(len(treatedData))]
    return test


def setVoltageA(voltage):
    '''set voltage, expects float value in Volts'''
    global DevNode
    global vNom
    global pause

    SD = b'\xD1'
    DN = bytes.fromhex(DevNode)
    OBJ = b'\x32'
    setValue = hex(int(voltage*25600.0/vNom)).replace("0x","").zfill(4)
    DATA1 = bytes.fromhex(setValue[:2])
    DATA2 = bytes.fromhex(setValue[2:])
    CS = checksum([SD, DN, OBJ, DATA1, DATA2])
    get_query = SD+DN+OBJ+DATA1+DATA2+CS
    ser.write(get_query)
    return 0;



#------------------------------Calculate floating point from integer functions--------------------------------------

def getMantissa(integer):
    '''turn int representation of 23 bit mantissa to the representation needed in the IEEE standard, see wikipedia'''
    res = 0.0
    for i in range(1, 24):
        res += 2**(-i)*((integer & (1 << (23-i))) >> (23-i))
    return res


def int2flp(uhex):
    '''method to convert int from readandtreat to floating point IEEE standard'''
    sign = uhex >> 31
    exponent = (uhex & (~0 >> 1)) >> 23
    mantissa = uhex & ~(~0 << 23)
    flp = 2**sign*(1+getMantissa(mantissa))*2**(exponent - 127)
    return flp

#-------------------------------------------------------------------------------------------------------------------
