import sys
from subprocess import call

#Load file and split on the hyphen
def LoadDataHyphen(fname):
    f=open(fname,'r')
    data=[]
    for line in f.readlines():
        data.append(line.replace('\n','').split('-'))
    f.close()
    return data

#Create a list of strings from a column in a file loaded with LoadDataHyphen
def IterativeStrAppend(values,index):
    new_list=[]
    for i in range(len(values)):
        point=str(values[i][index])
        new_list.append(point)
    return new_list

#Create a list of integers from a column in a file loaded with LoadDataHyphen
def IterativeIntAppend(values,index):
    new_list=[]
    for i in range(len(values)):
        point=int(values[i][index])
        new_list.append(point)
    return new_list


file = sys.argv[1] #input file with list of disks
diskout = sys.argv[2] #the disk to which all files will be symbolically linked
name = sys.argv[3] #name of the file being linked
n = int(sys.argv[4]) #number of the node currently working on

text = LoadDataHyphen(file) #load in text file containing disk information for all the files
new_node = IterativeIntAppend(text,0) #location of file on the new cluster
disks = IterativeStrAppend(text,1) #disk on which the file resides
nodes = IterativeIntAppend(text,2) #number following .node in the file name

valid_disks = ['disk1','disk2','disk3','disk4','a','b','c','d'] #list of perimissable file locations within a node

print n

node_file_1 = n - 111 #should be one of the .node file numbers
node_file_2 = node_file_1 + 8 #should be the other .node file number
node_files = [] #empty list created, later used to contain disk information for node files on node n
node_files2 = []#empty list created, later used to check existence of approrpiate .node files on each node
for i in range(len(nodes)):
	if new_node[i] != n: #if its not the current location, worry about it later
		pass
	if new_node[i] == n: #if it is the current location
		if disks[i] in valid_disks: #and it is a valid location
			if nodes[i] in node_files: #report if there are two of the same file on a single node
				print 'Duplicate .node{0} files on node{1}'.format(nodes[i],n)
			if nodes[i] not in node_files: 
				point = [new_node[i],disks[i],nodes[i]]
				node_files.append(point) #add disk information
				node_files2.append(nodes[i]) #add node file number
		if disks[i] not in valid_disks: #if not a valid location, discard the entry
			pass
print 'node_files created for node{0}'.format(n) #print a status update (mostly diagnostic)
j=0
while j < (len(node_files)): #now loop through accepted values and check cases
	node = node_files[j][2]
	disk = node_files[j][1]
	if node_file_1 not in node_files2 and node_file_2 not in node_files2: #if neither .node file number is on a given node, report it as an error 
		print 'Error: too both node files missing - sym linking process stopped on node{0} - user solution is required'.format(n)
		break
	if node_file_1 in node_files2 and node_file_2 not in node_files2: #if only one of the .node numbers is on a given node, follow steps below
		if node == node_file_1: #if the .node number matches the file that exists
			if disk == diskout: #and its on the same disk as we would like the output to appear, just move it to the specified directory
				print '.node{0} file in correct location already'.format(node_file_1)
				print 'Linking file:'
				print "/mnt/{0}/gsbuser/EoR/{1}.node{2}".format(diskout,name,node_file_1)
				print "to /mnt/{0}/gsbuser/EoR/{1}.node{2}".format(diskout,name,node_file_2)
				call(["ln","-s","/mnt/{0}/gsbuser/EoR/{1}.node{2}".format(diskout,name,node_file_1),"/mnt/{0}/gsbuser/EoR/{1}.node{2}".format(diskout,name,node_file_2)])
			if disk != diskout: #or its on another disk - then symbolic link it to the correct one
				print 'Linking file:'
				print "/mnt/{0}/gsbuser/EoR/{1}.node{2}".format(disk,name,node_file_1)
				print "to /mnt/{0}/gsbuser/EoR/{1}.node{2}".format(diskout,name,node_file_1)
                                call(["ln","-s","/mnt/{0}/gsbuser/EoR/{1}.node{2}".format(disk,name,node_file_1),"/mnt/{0}/gsbuser/EoR/{1}.node{2}".format(diskout,name,node_file_1)])
				print 'Linking file"'
				print "/mnt/{0}/gsbuser/EoR/{1}.node{2}".format(disk,name,node_file_1)
				print "to /mnt/{0}/gsbuser/EoR/{1}.node{2}".format(diskout,name,node_file_2)
				call(["ln","-s","/mnt/{0}/gsbuser/EoR/{1}.node{2}".format(disk,name,node_file_1),"/mnt/{0}/gsbuser/EoR/{1}.node{2}".format(diskout,name,node_file_2)])						
		j+=1
	if node_file_2 in node_files2 and node_file_1 not in node_files2: #if only one of the .node numbers is on a given node, follow steps below
		if node == node_file_2: #if the .node number matches the file that exists
			if disk == diskout: #and its on the same disk as we would like the output to appear, just move it to the specified directory
				print '.node{0} file in correct location already'.format(node_file_2)
				print 'Linking file:'
				print "/mnt/{0}/gsbuser/EoR/{1}.node{2}".format(diskout,name,node_file_2)
				print "to /mnt/{0}/gsbuser/EoR/{1}.node{2}".format(diskout,name,node_file_1)
				call(["ln","-s","/mnt/{0}/gsbuser/EoR/{1}.node{2}".format(diskout,name,node_file_2),"/mnt/{0}/gsbuser/EoR/{1}.node{2}".format(diskout,name,node_file_1)])
			if disk != diskout: #or is on another disk - then symbolic link it to the correct one
				print 'Linking file:'
				print "/mnt/{0}/gsbuser/EoR/{1}.node{2}".format(disk,name,node_file_2)
				print "to /mnt/{0}/gsbuser/EoR/{1}.node{2}".format(diskout,name,node_file_2)
				call(["ln","-s","/mnt/{0}/gsbuser/EoR/{1}.node{2}".format(disk,name,node_file_2),"/mnt/{0}/gsbuser/EoR/{1}.node{2}".format(diskout,name,node_file_2)])
				print 'Linking file:'
				print "/mnt/{0}/gsbuser/EoR/{1}.node{2}".format(disk,name,node_file_2)
				print "to /mnt/{0}/gsbuser/EoR/{1}.node{2}".format(diskout,name,node_file_1)
				call(["ln","-s","/mnt/{0}/gsbuser/EoR/{1}.node{2}".format(disk,name,node_file_2),"/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node_file_1)])				
		j+=1
	if node_file_2 in node_files2 and node_file_1 in node_files2: #if both .node number are present on the node, then move or link the file as depending on their current location
		if disk == diskout: 
			print '.node{0} file in correct location already'.format(node)
			j+=1
		if disk != diskout:
                        print 'Linking file:'
			print "/mnt/{0}/gsbuser/EoR/{1}.node{2}".format(disk,name,node)
			print "to /mnt/{0}/gsbuser/EoR/{1}.node{2}".format(diskout,name,node)
			call(["ln","-s","/mnt/{0}/gsbuser/EoR/{1}.node{2}".format(disk,name,node),"/mnt/{0}/gsbuser/EoR/{1}.node{2}".format(diskout,name,node)])
			j+=1
