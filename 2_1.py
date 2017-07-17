#!/usr/bin/python
import sys
listk=sys.argv[1].split(',') #list 1
listv=sys.argv[2].split(',') #list 2
i=0
dictout={}
while i <= (len(listk)-1):
	if i <= (len(listv)-1):
		dictout[listk[i]]=listv[i]
	else:
		dictout[listk[i]]=None	
	i+=1 
print listk
print listv
print dictout

