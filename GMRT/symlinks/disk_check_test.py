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
disk = IterativeStrAppend(text,1) #disk on which the file resides
node = IterativeIntAppend(text,2) #number following .node in the file name

valid_disks = ['disk1','disk2','disk3','disk4','a','b','c','d'] #list of perimissable file locations within a node

n = 111
while n < 119:
	i = 0
	while i < (len(node)):
		if disk[i] not in valid_disks:
			i+=1
		else:
			if new_node[i] == n:
				node_files = [] #empty list created, later used to check existence of approrpiate .node files on each node
				if node[i] in node_files:
					print 'Duplicate files'
					node_files.append(node[i])
				else:
					node_files.append(node[i])
				node_file_1 = n - 111 #should be one of the .node file numbers
				node_file_2 = node_file_1 + 8 #should be the other .node file number
				if node[i] == node_file_1: #if the .node file number matches node_file_1, define its disk number as disk1
					disk1 = disk[i]
				if node[i] == node_file_2: #if the .node file number matched node_file_2, define its disk number as disk2
					disk2 == disk[i]
				if node_file_1 and node_file_2 not in node_files: #if neither .node file number is on a given node, report it as an error and stop
					print 'node{0} {1} .node{2}'.format(n,disk[i],node[i])
					print 'Error: too many node files missing - sym linking process stopped at node{0}'.format(n)
				if node_file_1 in node_files and node_file_2 not in node_files: #if only one of the .node numbers is on a given node, follow steps below
					if node[i] == node_file_1: #if the .node number matches the file that exists
						if disk[i] == diskout: #and its on the same disk as we would like the output to appear, just move it to the specified directory
							old_node = 33 + node[i]
							print 'node{0} {1} .node{2}'.format(n,disk[i],node[i])
							print 'Moving file - Case 2, correct disk, existing file'
							#call(["mv", "/mnt/{0}/gsbuser/TSAS/node{1}/{2}.node{3]".format(diskout,old_node,name,node[i]), "/mnt/{0}/gsbuser/TSAS/".format(diskout)])
						if disk[i] != diskout: #or its on another disk - then symbolic link it to the correct one
							old_node = 33 + node[i]
							print 'node{0} {1} .node{2}'.format(n,disk[i],node[i])
							print 'Linking file - Case 2 incorrect disk, existing file'
							#call(["ln","-s","/mnt/{0}/gsbuser/TSAS/node{1}/{2}.node{3}".format(disk[i],old_node,name,node[i]),"/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node[i])])
					if node[i] == node_file_2: #if the .node number matches the file that doesn't exist
						if disk1 == diskout: #and the existing file is on the correct disk, then link the file to the existing file on the correct disk
							old_node = 33 + node[i]
							print 'node{0} {1} .node{2}'.format(n,disk[i],node[i])
							print 'Linking file - Case 2 correct disk, non-existing file'
							#call(["ln", "-s", "/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node_file_1), "/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node[i])])
						if disk1 != diskout: #or the existing file is on the wrong disk - then link the file to the existing file on the correct disk
							old_node = 33 + node[i]
							print 'node{0} {1} .node{2}'.format(n,disk[i],node[i])
							print 'Linking file - Case 2 incorrect disk, non-existing file'
							#call(["ln","-s","/mnt/{0}/gsbuser/TSAS/node{1}/{2}.node{3}".format(disk[i],old_node,name,node_file_1),"/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node[i])])
				if node_file_2 in node_files and node_file_1 not in node_files: #if only one of the .node numbers is on a given node, follow steps below
					if node[i] == node_file_2: #if the .node number matches the file that exists
						if disk[i] == diskout: #and its on the same disk as we would like the output to appear, just move it to the specified directory
							old_node = 33 + node[i]
							print 'node{0} {1} .node{2}'.format(n,disk[i],node[i])
							print 'Moving file - Case 3, correct disk, existing file'
							#call(["mv", "/mnt/{0}/gsbuser/TSAS/node{1}/{2}.node{3]".format(diskout,old_node,name,node[i]), "/mnt/{0}/gsbuser/TSAS/".format(diskout)])
						if disk[i] != diskout: #or its on another disk - then symbolic link it to the correct one
							old_node = 33 + node[i]
							print 'node{0} {1} .node{2}'.format(n,disk[i],node[i])
							print 'Linking file - Case 3, correct disk, existing file'
							#call(["ln","-s","/mnt/{0}/gsbuser/TSAS/node{1}/{2}.node{3}".format(disk[i],old_node,name,node[i]),"/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node[i])])
					if node[i] == node_file_1: #if the .node number matches the file that doesn't exist
						if disk1 == diskout: #and the existing file is on the correct disk, then link the file to the existing file on the correct disk
							old_node = 33 + node[i]
							print 'node{0} {1} .node{2}'.format(n,disk[i],node[i])
							print 'Linking file - Case 3, correct disk, non-existing file'
							#call(["ln", "-s", "/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node_file_2), "/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node[i])])
						if disk1 != diskout: #or the existing file is on the wrong disk - then link the file to the existing file on the correct disk
							old_node = 33 + node[i]
							print 'node{0} {1} .node{2}'.format(n,disk[i],node[i])
							print 'Linking file - Case 3, incorrect disk, non-existing file'
							#call(["ln","-s","/mnt/{0}/gsbuser/TSAS/node{1}/{2}.node{3}".format(disk[i],old_node,name,node_file_2),"/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node[i])])
				if node_file_2 and node_file_1 in node_files: #if both .node number are present on the node, then move or link the file as depending on their current location
					if disk[i] == diskout: 
						old_node = 33 + node[i]
						print 'node{0} {1} .node{2}'.format(n,disk[i],node[i])
						print 'Moving file - Case 4, correct disk, existing file'
						#call(["mv", "/mnt/{0}/gsbuser/TSAS/node{1}/{2}.node{3}".format(diskout,old_node,name,node[i]), "/mnt/{0}/gsbuser/TSAS/".format(diskout)])
					if disk[i] != diskout:
						old_node = 33 + node[i]
						print 'node{0} {1} .node{2}'.format(n,disk[i],node[i])
						print 'Linking file - Case 4, incorrect disk, existing file'
						#call(["ln","-s","/mnt/{0}/gsbuser/TSAS/node{1}/{2}.node{3}".format(disk[i],old_node,name,node[i]),"/mnt/{0}/gsbuser/TSAS/{1}.node{2}".format(diskout,name,node[i])])
		i+=1
	n+=1 #move to the next node to check it