import manage as man
import sys

fname=sys.argv[1]

seconds=man.LoadData(fname)
seconds=man.IterativeFloatAppend(seconds,0)

p0=1.60731438719155/1000

for i in range(len(seconds)):
    t=seconds[i]
    mod=t%p0
    iphase=16*t/p0
    iphase_board=iphase%16
    iphase_mod=((iphase+4000000*16)%16)
    diff1=iphase-iphase_board
    diff2=iphase-iphase_mod
    diff=diff1-diff2
    print iphase, iphase_mod, iphase_board, mod, diff
