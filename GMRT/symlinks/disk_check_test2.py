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

text = LoadDataHyphen(file) #load in text file containing disk information for all the files
new_node = IterativeIntAppend(text,0) #location of file on the new cluster
disks = IterativeStrAppend(text,1) #disk on which the file resides
nodes = IterativeIntAppend(text,2) #number following .node in the file name

valid_disks = ['disk1','disk2','disk3','disk4','a','b','c','d'] #list of perimissable file locations within a node

n = 111
while n < 119:
	#call
	print n
	node_file_1 = n - 111 #should be one of the .node file numbers
	node_file_2 = node_file_1 + 8 #should be the other .node file number
	node_files = [] #empty list created, later used to check existence of approrpiate .node files on each node
	node_files2 = []
	for i in range(len(nodes)):
		if new_node[i] != n:
			pass
		if new_node[i] == n:
			if disks[i] in valid_disks:
				if nodes[i] in node_files:
					print 'Duplicate files of node{0}'.format(nodes[i])
				if nodes[i] not in node_files:
					point = [new_node[i],disks[i],nodes[i]]
					node_files.append(point)
					node_files2.append(nodes[i])
			if disks[i] not in valid_disks:
				pass
	print 'node_files created for node{0}'.format(n)
	j=0
	while j < (len(node_files)):
		node = node_files[j][2]
		disk = node_files[j][1]
		print 'node file = .node{0}, disk = {1}'.format(node,disk)
		if node_file_1 not in node_files2 and node_file_2 not in node_files2: #if neither .node file number is on a given node, report it as an error and stop
			print 'node{0} {1} .node{2}'.format(n,disk,node)
			print 'Error: too many node files missing - sym linking process stopped at node{0}'.format(n)
			j+=1
		if node_file_1 in node_files2 and node_file_2 not in node_files2: #if only one of the .node numbers is on a given node, follow steps below
			if node == node_file_1: #if the .node number matches the file that exists
				if disk == diskout: #and its on the same disk as we would like the output to appear, just move it to the specified directory
					print 'node{0} {1} .node{2}'.format(n,disk,node)
					print 'Moving file - Case 2, correct disk, existing file'
					print "/mnt/{0}/gsbuser/TSAS/node{1}/{2}.node{3]".format(diskout,node_file_1+33,name,node_file_1)
					print "/mnt/{0}/gsbuser/TSAS/".format(diskout)
					call(["mv","/mnt/{0}/gsbuser/TSAS/node{1}/{2}.node{3]".format(diskout,node_file_1+33,name,node_file_1),"/mnt/{0}/gsbuser/TSAS/".format(diskout)])
					print 'node{0} {1} .node{2}'.format(n,disk,node+8)
					print 'Linking file - Case 2 correct disk, non-existing file'
					print "/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node_file_1)
					print "/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node_file_2)
					call(["ln","-s","/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node_file_1),"/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node_file_2)])
				if disk != diskout: #or its on another disk - then symbolic link it to the correct one
					print 'node{0} {1} .node{2}'.format(n,disk,node)
					print 'Linking file - Case 2 incorrect disk, existing file'
					print "/mnt/{0}/gsbuser/TSAS/node{1}/{2}.node{3}".format(disk,node_file_1+33,name,node_file_1)
					print "/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node_file_1)
					call(["ln","-s","/mnt/{0}/gsbuser/TSAS/node{1}/{2}.node{3}".format(disk,node_file_1+33,name,node_file_1),"/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node_file_1)])
					print 'node{0} {1} .node{2}'.format(n,disk,node+8)
					print 'Linking file - Case 2 incorrect disk, non-existing file'
					print "/mnt/{0}/gsbuser/TSAS/node{1}/{2}.node{3}".format(disk,node_file_1+33,name,node_file_1)
					print "/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node_file_2)
					call(["ln","-s","/mnt/{0}/gsbuser/TSAS/node{1}/{2}.node{3}".format(disk,node_file_1+33,name,node_file_1),"/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node_file_2)])						
			j+=1
		if node_file_2 in node_files2 and node_file_1 not in node_files2: #if only one of the .node numbers is on a given node, follow steps below
			if node == node_file_2: #if the .node number matches the file that exists
				if disk == diskout: #and its on the same disk as we would like the output to appear, just move it to the specified directory
					print 'node{0} {1} .node{2}'.format(n,disk,node)
					print 'Moving file - Case 3, correct disk, existing file'
					print "/mnt/{0}/gsbuser/TSAS/node{1}/{2}.node{3]".format(diskout,node_file_2+33,name,node_file_2)
					print "/mnt/{0}/gsbuser/TSAS/".format(diskout)
					call(["mv", "/mnt/{0}/gsbuser/TSAS/node{1}/{2}.node{3]".format(diskout,node_file_2+33,name,node_file_2),"/mnt/{0}/gsbuser/TSAS/".format(diskout)])
					print 'node{0} {1} .node{2}'.format(n,disk,node-8)
					print 'Linking file - Case 3, correct disk, non-existing file'
					print "/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node_file_2)
					print "/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node_file_1)
					call(["ln","-s","/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node_file_2),"/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node_file_1)])
				if disk != diskout: #or is on another disk - then symbolic link it to the correct one
					print 'node{0} {1} .node{2}'.format(n,disk,node)
					print 'Linking file - Case 3, incorrect disk, existing file'
					print "/mnt/{0}/gsbuser/TSAS/node{1}/{2}.node{3}".format(disk,node_file_2+33,name,node_file_2)
					print "/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node_file_2)
					call(["ln","-s","/mnt/{0}/gsbuser/TSAS/node{1}/{2}.node{3}".format(disk,node_file_2+33,name,node_file_2),"/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node_file_2)])
					print 'node{0} {1} .node{2}'.format(n,disk,node-8)
					print 'Linking file - Case 3, incorrect disk, non-existing file'
					print "/mnt/{0}/gsbuser/TSAS/node{1}/{2}.node{3}".format(disk,old_node,name,node_file_2)
					print "/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node_file_1)
					call(["ln","-s","/mnt/{0}/gsbuser/TSAS/node{1}/{2}.node{3}".format(disk,old_node,name,node_file_2),"/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node_file_1)])				
			j+=1
		if node_file_2 in node_files2 and node_file_1 in node_files2: #if both .node number are present on the node, then move or link the file as depending on their current location
			if disk == diskout: 
				old_node = 33 + node
				print 'node{0} {1} .node{2}'.format(n,disk,node)
				print 'Moving file - Case 4, correct disk, existing file'
				print  "/mnt/{0}/gsbuser/TSAS/node{1}/{2}.node{3}".format(diskout,old_node,name,node)
				print "/mnt/{0}/gsbuser/TSAS/".format(diskout)
				call(["mv","/mnt/{0}/gsbuser/TSAS/node{1}/{2}.node{3}".format(diskout,old_node,name,node),"/mnt/{0}/gsbuser/TSAS/".format(diskout)])
				j+=1
			if disk != diskout:
				old_node = 33 + node
				print 'node{0} {1} .node{2}'.format(n,disk,node)
				print 'Linking file - Case 4, incorrect disk, existing file'
				print "/mnt/{0}/gsbuser/TSAS/node{1}/{2}.node{3}".format(disk,old_node,name,node)
				print "/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node)
				call(["ln","-s","/mnt/{0}/gsbuser/TSAS/node{1}/{2}.node{3}".format(disk,old_node,name,node),"/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node)])
				j+=1
	n+=1 #move to the next node to check it
