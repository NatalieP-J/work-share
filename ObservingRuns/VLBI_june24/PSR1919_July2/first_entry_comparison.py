import manage as man
import numpy as np

def Comparison(values):
    newlist=[]
    for i in range(len(values)):
        for j in range(len(values)):
            point=abs(values[i]-values[j])
            point=[i, j, point]
            newlist.append(point)
    return newlist

first_entry=[]
n=33
while n < 40:
    i=1
    while i < 5:
        fname='node{0}_july2/EoR/timestamp_voltage.all.1919_2_july2.{1}.dat'.format(n,i)
        try:
            times=man.LoadData(fname)
            year=man.IterativeIntAppend(times,0)
            month=man.IterativeIntAppend(times,1)
            day=man.IterativeIntAppend(times,2)
            hour=man.IterativeIntAppend(times,3)
            minute=man.IterativeIntAppend(times,4)
            seconds=man.IterativeIntAppend(times,5)
            frac=man.IterativeFloatAppend(times,6)

            time=[]
            for j in range(len(times)):
                point=(day[j]*3600*24)+(hour[j]*3600)+(minute[j]*60)+(seconds[j])+(frac[j])
                time.append(point)        


            first=time[0]
            first_entry.append(first)
            i+=1
 
        except IOError:
            print "Missing node{0}/EoR/timestamp_voltage.all.1919_2_july2.{1}.dat".format(n,i)
            i+=1
            pass
    n+=1

check=Comparison(first_entry)

    
