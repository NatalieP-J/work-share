from manage import *
import sys

def WriteFileCols(values1,values2,fname):
    with open(fname,"w") as data:
        for i in range(len(values1)):
            data.write("{0}\t{1}\n".format(values1[i], values2[i]))
    
data1=LoadData(sys.argv[1]) #file containing tjd
data2=LoadData(sys.argv[2]) #file containing gst
name=sys.argv[3]
tjd=IterativeFloatAppend(data1,0)
gst=IterativeFloatAppend(data2,0)

WriteFileCols(tjd,gst,name)
