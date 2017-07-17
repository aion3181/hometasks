#!/usr/bin/python
import sys
ffp=sys.argv[1] #access.log file
#print ffp
f = open(ffp, 'r')
list2=[]
for line in f:
	list1 = line.split(' ')
	list2.append(list1[0])  #list of ip
f.close()
#print list2
dict1={}
for ip in list2:
	keyip=list2.count(ip)
	dict1[ip]=keyip
#print dict1
k=1
for key, value in sorted(dict1.items(), key=(lambda item: (item[1], item[0])), reverse=True):
	if k<=10:
		print ("%s: %s" % (key, value))
	k+=1

