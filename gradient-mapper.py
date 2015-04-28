#!/usr/bin/python

# Format of each line is:
#Input: userID::movieID::ratings::timestamp

import sys
import re

# Passing arguments isForW -mapper 'mapper.py arg1 arg2'
isForW = False
if sys.argv[1] == "isForW":
	isForW = True

for line in sys.stdin:
	if not line.strip(): 
        	continue
	data = re.split('\t|\:{2}', line.strip())
	
	# send a whole line of V to a reducer	
	# emit userID,movieID,ratings --> emit(i,j,v)
	if len(data) >= 3:
		userID, movieID, ratings, timestamp = data
		if isForW:
			key = int(userID) - 1
			value = str(int(movieID) - 1) + ',' + str((float(ratings)-3)/2.0)
		else:
			key = int(movieID) - 1
			value = str(int(userID) - 1) + ',' + str((float(ratings)-3)/2.0)
		print '%s\t%s' % (key, value)
