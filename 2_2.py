#!/usr/bin/python
import sys
testtext=sys.argv[1]   #text to check
i=0
b= len(testtext)
while i <= (b//2)-1:
	if testtext[i:i+1] is not testtext[(b-1-i):(b-i)]:
		print 'not a palindrome word'
		break
	i+=1
else:
	print 'palindrome word'
