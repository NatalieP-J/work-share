#!/usr/bin/env python
import os
import numpy as np

path='.'

for dirName, subdirList, fileList in os.walk(path):
    print ('Found directory: %s' % dirName)
    for fname in fileList:
        if fname='Horizons.h5':
            print('\t%s' % fname)
   

