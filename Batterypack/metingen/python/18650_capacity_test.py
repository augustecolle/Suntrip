import EAEL9080 as au
import time as tm
import csv

logtime = 1                         # seconds
numlines = 1000                     # lines in each csv file
name = 'test_auto_12cells'              # name of CSV files

cyclelog = 0
csv_i = 0                           # csv counter
header = ['Tijd', 'Spanning', 'Stroom']
volts = [None]*numlines
amps = [None]*numlines
times = [None]*numlines

au.startSerial()
au.setRemoteControllOn()

au.setCCMode()
tm.sleep(.5)
au.setCurrentA(5*5)                 # in amps; .5A estimated motor use
au.setVoltageA(37.4)                 # in volts
au.setPowerA(1200)
au.clearBuffer()


def write2csv(name, data, header):
    '''method to write data to csv'''
    header = header
    data = zip(*data)
    with open(listname, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(header)
        writer.writerows(data)


while(au.getActualValues()[0] > (37.4)):
    start = tm.time()
    temp = au.getActualValues()
    print("Discharging cycle log: " + str(cyclelog))
    print("[Voltage, Current, Power]: " + str(temp))
    volts[cyclelog] = temp[0]
    amps[cyclelog] = temp[1]
    times[cyclelog] = tm.strftime("%H:%M:%S", tm.localtime())
    cyclelog += 1
    if (cyclelog >= numlines):
        cyclelog = 0                # reset counter
        listname = name+str(csv_i).zfill(4)+'.csv'
        write2csv(listname, [times, volts, amps], header)
        csv_i += 1                  # increase counter for csv files
        volts = [None]*numlines
        amps = [None]*numlines
        times = [None]*numlines
    # now wait untill one second passed since beginning of cycle
    tm.sleep(logtime - (tm.time() - start))

print("Cut-off voltage reached!")
print("Last recorded voltage: {:>5.2f}".format(temp[0]))
listname = name+str(csv_i).zfill(4)+'.csv'

write2csv(listname, [times, volts, amps], header)

au.setCurrentA(0)
au.setVoltageA(0)
au.setPowerA(0)
au.setInputOff()
au.setRemoteControllOff()
au.stopSerial()
