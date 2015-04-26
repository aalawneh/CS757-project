#!/usr/bin/env python

import sys
import numpy
import os

try:
    import numpy
except:
    print "This implementation requires the numpy module."
    exit(0)

def main():
	try:
		os.system("rm -rf part-00000")
	except:
		print ""

	try:
		os.system("hadoop fs -rm  -r proj/output/")
	except:
		print ""

	#os.system("hadoop fs -mkdir proj/input");	
	#os.system("hadoop fs -put V.arr proj/input");

	# Data dimensions 49
	rdim = 19
	# len(V) The number of rows in V - For Faces dataset it is 361
	# This is the number of users
	vdim = 943 
	# len(input[0]) The number of columns in V - For Faces dataset it is 2429
	samples = 1682 
	
	# 943 x 1682 = 1586126	

	# Create initial matrices: 
	# vdim-by-rdim matrix of normally distributed random numbers.
	W = abs(numpy.random.rand(vdim,rdim))
	# rdim-by-samples matrix of normally distributed random numbers.
	H = abs(numpy.random.rand(rdim,samples))
	
	# Save W and H to a file
	numpy.savetxt('w.arr', W, '%.18e', delimiter=' ')
	numpy.savetxt('h.arr', H, '%.18e', delimiter=' ')

	# Initial stepsizes
	stepsizeW = 1;
	stepsizeH = 1;

	# Start iteration
	iter = 0;

	while True:
		iter += 1;
		# ***** This is for W *****
		isForW = True;

		# Gradient for W
		# Map/Reduce Job 1
                # ####  Maper: send one V row to the reducer
		# ####  Reducer: calculate the gradient dW = (W*H-V)*H'
		os.system("hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.1.1.jar  -input proj/input/100K-ratings.dat -output proj/output/ -mapper 'job1Mapper.py isForW' -reducer 'job1Reducer.py isForW'  -file job1Mapper.py -file job1Reducer.py  -cacheFile proj/input/w.arr#w.arr -cacheFile proj/input/h.arr#h.arr")
		
		# save dW
		os.system("hadoop fs -get proj/output/part-00000")
		os.system("mv part-00000 dW.arr")

		dW = numpy.zeros((vdim,rdim))
		wFile = open ( 'dW.arr' , 'r')
		for line in wFile:
			data = line.split('\t', 1)
			index, vector = data
			vector = vector.split(',')
			dW[index,:] = vector

		# clean up
		os.system("hadoop fs -rm proj/output/*")

		while True:
			# Update W --> Wnew = W- stepsize * dW
			W = numpy.subtract(W, dW)
			numpy.savetxt('w.arr', W, '%.18e', delimiter=' ')
			# do the projection
			
			# calculate the cost


		# ***** This is for H *****
		isForW = False;

		# Gradient for H
		# Map/Reduce Job 1
                # ####  Maper: send one V column to the reducer
		# ####  Reducer: calculate the gradient dH = W'*(W*H-V);
		os.system("hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.1.1.jar  -input proj/input/100K-ratings.dat -output proj/output/ -mapper 'job1Mapper.py isForH' -reducer 'job1Reducer.py isForH'  -file job1Mapper.py -file job1Reducer.py  -cacheFile proj/input/w.arr#w.arr -cacheFile proj/input/h.arr#h.arr")
		
		# save dW
		os.system("hadoop fs -get proj/output/part-00000")
		os.system("mv part-00000 dH.arr")
		
		dH = numpy.zeros((rdim,samples))
		wFile = open ( 'dH.arr' , 'r')
		for line in wFile:
			data = line.split('\t', 1)
			index, vector = data
			vector = vector.split(',')
			dH[:,index] = vector

		# clean up
		os.system("hadoop fs -rm proj/output/*")

		while True:
			# Update H --> Hnew = H- stepsize * dH
			H = numpy.subtract(H, dH)
			numpy.savetxt('h.arr', H, '%.18e', delimiter=' ')
			
			# do the projection
			
			# calculate the cost

		if iter > 50: # When to break
			break
if __name__ == "__main__":
    main()

