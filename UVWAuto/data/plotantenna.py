import numpy as np
import manage as man
#import matplotlib.pylab as plt

data=man.LoadData('pycoords60_2013.dat')
x=man.IterativeFloatAppend(data,0)
y=man.IterativeFloatAppend(data,1)
z=man.IterativeFloatAppend(data,2)
test=man.LoadData('../UVW/May16first1919UVW.dat')
u=man.IterativeFloatAppend(test,4)
v=man.IterativeFloatAppend(test,6)
w=man.IterativeFloatAppend(test,8)
#plt.plot(x,y,'o',color='blue')
#plt.show()
