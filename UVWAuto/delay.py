import manage as man
import sys

#Function that writes two lists to file in columns
def WriteFileCols(values1,values2,fname):
    with open(fname,"w") as data:
        for i in range(len(values1)):
            data.write("{0}\t{1}\n".format(values1[i],values2[i]))

#Load data from file, splitting on two spaces
def LoadDataSpace(fname):
    f=open(fname,'r')
    data=[]
    for line in f.readlines():
        data.append(line.replace('\n','').split('  '))
    f.close()
    return data

#import the file containing the delays
fname=sys.argv[1]
#create a list of the rows in the files
data=LoadDataSpace(fname)
#a list of delay AND paralactic angle - only one space between these two, so 
#they were not split when imported
glomp=man.IterativeStrAppend(data,4)
#Antenna number: order is C(Centre)W(West)E(East)S(South)
antenna=man.IterativeIntAppend(data,1)

#modify glomp so it only contains delay, removing parallactic angle
delay=[]
for i in range(len(glomp)):
    point=float(glomp[i][:-9])
    delay.append(point)

#write the results to file - one column antenna number, the other delays
WriteFileCols(antenna,delay,"delay_{0}".format(fname))
