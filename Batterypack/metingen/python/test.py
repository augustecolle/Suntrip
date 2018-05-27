import DMM4050
import csv
import time as tm
import sys

multimeter = DMM4050.multimeter("10.128.21.167", 3490)

logtime = 1                         # seconds
numlines = 1000                     # lines in each csv file
name = '18650_littokala_baptist'    # name of CSV files
header = ['Tijd', 'Spanning', 'Stroom']

cyclelog = 0
csv_i = 0                           # csv counter
header = ['Tijd', 'Spanning', 'Stroom']
volts = [None]*numlines
amps = [None]*numlines
times = [None]*numlines


def write2csv(name, data, header_):
    '''method to write data to csv'''
    header = header_
    data = zip(*data)
    with open(listname, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(header)
        writer.writerows(data)


temp = multimeter.getVoltage(5)
while (True):
    try:
        start = tm.time()
        mv = multimeter.getVoltage(5)
        mi = multimeter.getCurrent(5)
        volts[cyclelog] = mv
        amps[cyclelog] = mi
        times[cyclelog] = tm.strftime("%H:%M:%S", tm.localtime())
        print("{:<10} {:+.2f} V".format("Spanning:", mv))
        print("{:<10} {:+.2f} A".format("Stroom:", mi))
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
    except:
        print(sys.exc_info())
        print("Unexpected error, writing to csv")
        # listname = name+str(csv_i).zfill(4)+'.csv'
        # write2csv(listname, [times, volts, amps], header)
        break

print("Cut-off voltage reached!")
print("Last recorded voltage: {:>5.2f}".format(mv))

listname = name+str(csv_i).zfill(4)+'.csv'
write2csv(listname, [times, volts, amps], header)
