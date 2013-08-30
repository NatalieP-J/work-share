import sys
#this program creates a file based on a start and end time that is formatted
#to be converted to tjd by convert_timestamp.perl
#file name for output
fname=sys.argv[1]
nanoseconds=15.
samples=2.**24
#rate of timestamps
rate=(nanoseconds/10**9)*samples
#start time of file
start=raw_input('''Enter the first time in the timestamp file\n Format Sat Jun 29 03:53:00.66: ''')
end=float(raw_input('''Enter the number of seconds total in the interval: '''))
#Write the file 
with open(fname,"w") as data:
    data.write("{0}\n".format(start))
    i=0
    while i<= (end):
        data.write("{0}\n".format(i))
        print 'working {0}'.format(float(i)/end)
        i+=rate
    
