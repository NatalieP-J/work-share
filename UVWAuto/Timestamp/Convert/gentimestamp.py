nanoseconds=15.
samples=2.**24
rate=(nanoseconds/10**9)*samples
with open('GeneratedTimeStamps.dat',"w") as data:
    data.write("Sat Jun 29 03:53:00.660051 IST 2013\n")
    i=0
    while i<= (1083+rate):
        data.write("{0}\n".format(i))
        i+=rate
    
