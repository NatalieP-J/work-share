from astropy.time import Time
import manage as man

fname="Timestamp/timestamp_voltage.b1957+20.raw0.node0.scan0"
times=man.LoadData(fname)
year=man.IterativeStrAppend(times,0)
month=man.IterativeStrAppend(times,1)
day=man.IterativeStrAppend(times,2)
hour=man.IterativeStrAppend(times,3)
minute=man.IterativeStrAppend(times,4)

seconds=[]
for i in range(len(times)-2):
    a=man.IterativeIntAppend(times,5)
    b=man.IterativeFloatAppend(times,6)
    point=a[i]+b[i]
    seconds.append(point)

time=[]
for i in range(len(times)-2):
    point="{0}-{1}-{2} {3}:{4}:{5}".format(year[i],month[i],day[i],hour[i],minute[i],seconds[i])
    time.append(point)

t=Time(time, scale='utc')
mjd=t.mjd

tjd=[]
for i in range(len(mjd)):
    date=mjd[i]-40000
    tjd.append(date)
fname="timestamp_voltage.b1957+20.raw0.node0.scan0"
man.WriteFile(tjd,"mod{0}.dat".format(fname))

