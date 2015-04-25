#!/usr/bin/python

# Format of each line is:
#Input: userID::movieID::ratings::timestamp

import sys
import re

# Passing arguments isForW -mapper 'count_mapper.py arg1 arg2'
# arg1 = sys.argv[1]
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
			key = movieID 
			value = userID + ',' + ratings
		else:
			key = userID
			value = movieID + ',' + ratings
		print '%s\t%s' % (key, value)
