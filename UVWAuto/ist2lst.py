
def ist2lst(ist, year, month, day):
    import sidereal
    import datetime
    import numpy as np


    gmrt_lat_deg = 19.0965167
    gmrt_lon_deg = 74.0497417
    gmrt_lat_rad = gmrt_lat_deg * np.pi / 180.0
    gmrt_lon_rad = gmrt_lon_deg * np.pi / 180.0
    gmrt = sidereal.LatLon(gmrt_lat_rad, gmrt_lon_rad)
    
    lst = []

    for it in ist:

        # hack for saying the observation starts late on the previous day
        # good as long end of observation isn't later in the day than beginning
        if it > ist[-1]: dd = day-1

        hh = int(it)
        mmss = (it - int(it))*60
        mm = int(mmss)
        ss = int((mmss - int(mmss))*60)
        
        time = datetime.datetime(year, month, dd, hh, mm, ss)
        time -= datetime.timedelta(hours=5, minutes=30) # UTC time
        
        gst = sidereal.SiderealTime.fromDatetime(time)
        thislst = gst.lst(gmrt.lon)

        

        #lst.append("%02dh%02dm" % (thislst.hour, thislst.minute))
        lst.append(thislst.hours)

    return lst

### EXAMPLE
#import numpy as np
#times256 = np.genfromtxt('times256.dat')
#ist = times256[:,1]*24.0/(2.0*np.pi)
#ist = np.where(ist<0, ist+24, ist)
#lst = ist2lst(ist)

