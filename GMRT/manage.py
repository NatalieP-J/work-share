#Loads a list of the rows in the file f, splitting on the spaces
def LoadData(fname):
    f=open(fname,'r')
    data=[]
    for line in f.readlines():
        data.append(line.replace('\n','').split(' '))
    f.close()
    return data

#Loads a list of the rows in the file f, splitting on the double spaces
def LoadDataSpaces(fname):
    f=open(fname,'r')
    data=[]
    for line in f.readlines():
        data.append(line.replace('\n','').split('  '))
    f.close()
    return data

#Loads a list of the rows in the file f, splitting on the tabs
def LoadDataTab(fname):
    f=open(fname,'r')
    data=[]
    for line in f.readlines():
        data.append(line.replace('\n','').split('\t'))
    f.close()
    return data

def LoadDataHyphen(fname):
    f=open(fname,'r')
    data=[]
    for line in f.readlines():
        data.append(line.replace('\n','').split('-'))
    f.close()
    return data

#Used in conjunction with LoadData to pull out a column of a file as a list
#of floats
def IterativeFloatAppend(values,index):
    new_list=[]
    for i in range(len(values)):
        point=float(values[i][index])
        new_list.append(point)
    return new_list

#Used in conjunction with LoadData to pull out a column of a file as a list
#of integers
def IterativeIntAppend(values,index):
    new_list=[]
    for i in range(len(values)):
        point=int(values[i][index])
        new_list.append(point)
    return new_list

#Used in conjunction with LoadData to pull out a column of a file as a list
#of strings
def IterativeStrAppend(values,index):
    new_list=[]
    for i in range(len(values)):
        point=str(values[i][index])
        new_list.append(point)
    return new_list

#Find the differences in consecutive values of a list
def Differences(values):
    new_list=[]
    for i in range((len(values))-1):
        point=values[i+1]-values[i]
        new_list.append(point)
    return new_list

#Remove repeats from a list of values
def RemoveRepeats(values):
    new_list=[]
    for i in range(len(values)):
        if values[i] not in new_list:
            new_list.append(values[i])
    return new_list

#Write a list to file as a column
def WriteFile(values,fname):
    with open(fname,"w") as data:
        for i in range(len(values)):
            data.write("{0}\n".format(values[i]))

def WriteFile2Cols(values1,values2,fname):
    with open(fname,"w") as data:
        for i in range(len(values1)):
            data.write("{0} {1}\n".format(values1[i],values2[i]))

def WriteFileCols(values,fname):
    with open(fname,"w") as data:
        for i in range(len(values)):
            data.write("{0} {1}\n".format(values[i][0],values[i][1]))

def WriteFile3Cols(values,fname):
    with open(fname,"w") as data:
        for i in range(len(values)):
            data.write("{0} {1} {2}\n".format(values[i][0],values[i][1],values[i][2]))

def WriteFile5Cols(values,fname):
    with open(fname,"w") as data:
        for i in range(len(values)):
            data.write("{0} {1} {2} {3} {4}\n".format(values[i][0],values[i][1],values[i][2],values[i][3],values[i][4]))

def WriteFile4Cols(values,fname):
    with open(fname,"w") as data:
        for i in range(len(values)):
            data.write("{0} {1} {2} {3}\n".format(values[i][0],values[i][1],values[i][2],values[i][3]))

def WriteFile6Cols(values,fname):
    with open(fname,"w") as data:
        for i in range(len(values)):
            data.write("{0} {1} {2} {3} {4} {5}\n".format(values[i][0],values[i][1],values[i][2],values[i][3],values[i][4],values[i][5]))

def WriteFile7Cols(values,fname):    
    with open(fname,"w") as data:
        for i in range(len(values)):
            data.write("{0} {1} {2} {3} {4} {5} {6}\n".format(values[i][0],values[i][1],values[i][2],values[i][3],values[i][4],values[i][5],values[i][6]))

def WriteFile8Cols(values,fname):
    with open(fname,"w") as data:
        for i in range(len(values)
            data.write("{0} {1} {2} {3} {4} {5} {6} {7}\n".format(values[i][0],values[i][1],values[i][2],values[i][3],values[i][4],values[i][5],values[i][6],values[i][7]))

