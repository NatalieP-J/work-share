def LoadRateData(fname):
    f=open(fname,'r')
    data=[]
    for line in f.readlines():
        data.append(line.replace('\n','').split(' '))
    f.close()
    data.pop(0)
    return data

def Rate(somelist):
    rate = []
    for i in range(len(somelist)-1):
        rate.append(somelist[i+1]-somelist[i])
    return rate
        
