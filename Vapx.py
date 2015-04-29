#!/usr/bin/env python

import sys
import os
import re

try:
    import numpy as np
except:
    print "This implementation requires the numpy module."
    exit(0)

wf = open ( 'w.arr' , 'r')
W = [ map(float,line.split()) for line in wf ]

hf = open ( 'h.arr' , 'r')
H = [ map(float,line.split()) for line in hf ]

Vapx = np.dot(W, H)*2+3
np.savetxt('Vapx.arr', Vapx, '%.18e', delimiter=' ')

#try:
#    input_file = os.environ['mapreduce_map_input_file']
#except KeyError:
#    input_file = os.environ['map_input_file']
#input_file = input_file.split('/')[-3]
input_file = None
if input_file == "m-10M":
	moviesFileName = "10M-movies.dat"
elif input_file == "m-1M":
	moviesFileName = "1M-movies.dat"
else:
	moviesFileName = "100K-movies.dat"

moviesDict = {}

for line in open(moviesFileName):
	movieInfo = re.split('\||\:{2}', line)
	movieID = movieInfo[0]
	movieName = movieInfo[1]
	moviesDict[movieID] = movieName

suggestedMovies = [0.0, 0.0, 0.0, 0.0, 0.0]
print "Movie Suggestions:"
print "------------------"
for i in xrange(len(Vapx)):
	print "userID = %s" % (i+1)
    	for j in xrange(len(Vapx[i])):
		rating = Vapx[i][j]
		if (any(rating > r for r in suggestedMovies)):
			suggestedMovies.remove(min(suggestedMovies))
			suggestedMovies.append(j)
	print suggestedMovies
	for m in xrange(len(suggestedMovies)):
		m = m + 1
		movieName = moviesDict[str(m)]
           	print '%s' % (movieName)
	print "-------------------------------------------"
	suggestedMovies = [0.0, 0.0, 0.0, 0.0, 0.0]
