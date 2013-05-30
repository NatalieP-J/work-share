#!/usr/bin/env python

#this code will take positions in right ascension and declination and use them 
#to model an orbit.

import ephem
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt


ra=[12.65123,12.52769,12.02193,12.00482,12.15603,12.40213,12.74932]
dec=[-11.3902,-11.4058,-11.7345,-12.0093,-11.8321,-11.5896,-11.2302]


plt.plot(ra,dec,'o')
plt.xlim([0,24])
plt.ylim([-90,90])
plt.show()
