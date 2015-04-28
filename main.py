#!/usr/bin/env python

import sys
import os

try:
    import numpy as np
except:
    print "This implementation requires the numpy module."
    exit(0)
	
#this will differ by environment
#streaming_jar = "/usr/local/Cellar/hadoop/2.6.0/libexec/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar"
#streaming_jar = "/usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.1.1.jar"
#hydra
streaming_jar = "/apps/hadoop-2/share/hadoop/tools/lib/hadoop-streaming-2.4.1.jar -D mapred.reduce.tasks=30"


# different input files
input_file = "proj/input/100K-ratings.dat"

def projfunc(s, k1, k2):
	return s
	# this will be a mapreduce job later
	n = len(s)

	v = s + (k1-sum(s))/n

	zerocoeff = []
    
	while True:
		mid = np.ones(n)*k1/(n-len(zerocoeff))
		mid[zerocoeff] = 0
		w = v - mid
		a = sum(np.square(w))
		b = 2*np.dot(w,v)
		c = sum(np.square(v))-k2
		alphap = (-b+np.sqrt(b**2-4*a*c))/(2*a)
		v = alphap*w + v

		if all(v>=0):
			break
            
		zerocoeff = np.nonzero(v<=0)
		v[zerocoeff] = 0
		tempsum = sum(v)
		v = v + (k1-tempsum)/(n-len(zerocoeff))
		v[zerocoeff] = 0
    
	return v

def calc_cost():
	os.system("hadoop fs -put hnew.arr proj/input")
	os.system("hadoop fs -put wnew.arr proj/input")
	os.system("hadoop jar " + streaming_jar + " -input " + input_file + " -output proj/output/ -mapper 'cost-mapper.py 1000' -reducer 'cost-reducer.py'  -file cost-mapper.py -file cost-reducer.py  -cacheFile proj/input/wnew.arr#wnew.arr -cacheFile proj/input/hnew.arr#hnew.arr")

	os.system("hadoop fs -cat proj/output/part* > part-00000")
	os.system("hadoop fs -rm -r proj/output")
	os.system("hadoop fs -rm proj/input/hnew.arr")
	os.system("hadoop fs -rm proj/input/wnew.arr")
	
	count = 0
	sse = 0
	costFile = open ( 'part-00000' , 'r')
	for line in costFile:
		data = line.split('\t')
		count += int(data[0])
		sse += float(data[1])
	
	rmse = np.sqrt(sse/count)
	print "Current RMSE: %s" % rmse
	os.system("rm part-00000")
	return rmse


def main():
	try:
		os.system("hadoop fs -mkdir proj")
		os.system("hadoop fs -mkdir proj/input")
	except:
		print ""
	
	try:
		os.system("hadoop fs -put 100K-ratings.dat proj/input/")
	except:
		print ""

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
	# sparseness constraints for W and H
	sW = 0.01
	sH = 0.01
	# epsilon value for convergence detection
	epsilon = 1e-5
	W_converged = False
	H_converged = False

	# Create initial matrices: 
	# vdim-by-rdim matrix of normally distributed random numbers.
	W = np.random.randn(vdim,rdim)
	# rdim-by-samples matrix of normally distributed random numbers.
	H = np.random.randn(rdim,samples)
	#H = np.divide(H,np.dot(np.sum(np.square(H),1).reshape(rdim,1),np.ones((1,samples))))
	if sW != None:
		L1a = np.sqrt(vdim)-(np.sqrt(vdim)-1)*sW
		for i in range(0,rdim):
			W[:,i] = projfunc(W[:,i],L1a,1)
	if sH != None:
		L1s = np.sqrt(samples)-(np.sqrt(samples)-1)*sH
		for i in range(0,rdim):
			H[i,:] = projfunc(H[i,:],L1s,1)
        
	
	# Save W and H to a file
	np.savetxt('w.arr', W, '%.18e', delimiter=' ')
	np.savetxt('h.arr', H, '%.18e', delimiter=' ')
	
	# initial cost
	os.system("cp w.arr wnew.arr")
	os.system("cp h.arr hnew.arr")
	
	try:
		os.system("hadoop fs -put w.arr proj/input")
	except:
		os.system("hadoop fs -rm proj/input/w.arr")
		os.system("hadoop fs -put w.arr proj/input")
	try:
		os.system("hadoop fs -put h.arr proj/input")
	except:
		os.system("hadoop fs -rm proj/input/h.arr")
		os.system("hadoop fs -put h.arr proj/input")

	cost = calc_cost()

	# Initial stepsizes
	stepsizeW = 0.1;
	stepsizeH = 0.1;

	# Start iteration
	iter = 0;

	while True:
		iter += 1;
		print "Iteration %s" % iter
		
		if W_converged == False:
			if sW != None:
				# ***** This is for W *****
				print "# ************************ This is for W ************************"
				print "# ************************ This is for W ************************"
				print "# ************************ This is for W ************************"
				isForW = True;

				# Gradient for W
				# Map/Reduce Job 1
				# ####  Mapper: send one V row to the reducer
				# ####  Reducer: calculate the gradient dW = (W*H-V)*H'
				os.system("hadoop jar " + streaming_jar + " -input " + input_file + " -output proj/output/ -mapper 'gradient-mapper.py isForW' -reducer 'gradient-reducer.py isForW'  -file gradient-mapper.py -file gradient-reducer.py  -cacheFile proj/input/w.arr#w.arr -cacheFile proj/input/h.arr#h.arr")

				# save dW
				os.system("hadoop fs -cat proj/output/part* > part-00000")
				os.system("mv part-00000 dW.arr")

				dW = np.zeros((vdim,rdim))
				wFile = open ( 'dW.arr' , 'r')
				for line in wFile:
					data = line.split('\t', 1)
					index, vector = data
					vector = vector.split(',')
					dW[index,:] = vector

				# clean up
				os.system("hadoop fs -rm -r proj/output/")

				while True:
					# Update W --> Wnew = W- stepsize * dW
					Wnew = np.subtract(W, stepsizeW*dW)

					# do the projection
					for i in range(0,rdim):
						Wnew[:,i] = projfunc(Wnew[:,i],L1a,1)

					np.savetxt('wnew.arr', Wnew, '%.18e', delimiter=' ')

					# calculate the cost
					new_cost = calc_cost()

					if new_cost < cost:
						cost = new_cost
						break

					stepsizeW = stepsizeW/2
					if stepsizeW < epsilon:
						print "W converged. RMSE: %s" % cost
						W_converged = True
						if H_converged:
							return
						else:
							break

				#increase step size for next iteration
				stepsizeW = stepsizeW*1.2
				W = Wnew

			else:
				os.system("hadoop jar " + streaming_jar + " -input " + input_file + " -output proj/output/ -mapper 'nonsparseupdate-mapper.py isForW' -reducer 'nonsparseupdate-reducer.py isForW'  -file nonsparseupdate-mapper.py -file nonsparseupdate-reducer.py  -cacheFile proj/input/w.arr#w.arr -cacheFile proj/input/h.arr#h.arr")

				# save dW
				os.system("hadoop fs -cat proj/output/part* > part-00000")

				wFile = open ( 'part-00000' , 'r')
				for line in wFile:
					data = line.split('\t', 1)
					index, vector = data
					vector = vector.split(',')
					W[index,:] = vector

				# clean up
				os.system("rm part-00000")
				os.system("hadoop fs -rm -r proj/output/")

				# display current cost
				np.savetxt('wnew.arr', W, '%.18e', delimiter=' ')
				cost = calc_cost()

			np.savetxt('w.arr', W, '%.18e', delimiter=' ')
			os.system("hadoop fs -rm proj/input/w.arr")
			os.system("hadoop fs -put w.arr proj/input")

		if H_converged == False:
			if sH != None:
				# ************************ This is for H ************************
				print "# ************************ This is for H ************************"
				print "# ************************ This is for H ************************"
				print "# ************************ This is for H ************************"

				isForW = False;

				# Gradient for H
				# Map/Reduce Job 1
				# ####  Mapper: send one V column to the reducer
				# ####  Reducer: calculate the gradient dH = W'*(W*H-V);
				os.system("hadoop jar " + streaming_jar + " -input " + input_file + " -output proj/output/ -mapper 'gradient-mapper.py isForH' -reducer 'gradient-reducer.py isForH'  -file gradient-mapper.py -file gradient-reducer.py  -cacheFile proj/input/w.arr#w.arr -cacheFile proj/input/h.arr#h.arr")

				# save dH
				os.system("hadoop fs -cat proj/output/part* > part-00000")
				os.system("mv part-00000 dH.arr")

				dH = np.zeros((rdim,samples))
				wFile = open ( 'dH.arr' , 'r')
				for line in wFile:
					data = line.split('\t', 1)
					index, vector = data
					vector = vector.split(',')
					dH[:,index] = vector

				# clean up
				os.system("hadoop fs -rm -r proj/output/")

				while True:
					# Update H --> Hnew = H- stepsize * dH
					Hnew = np.subtract(H, stepsizeH*dH)


					# do the projection
					for i in range(0,rdim):
						Hnew[i,:] = projfunc(Hnew[i,:],L1s,1)

					np.savetxt('hnew.arr', Hnew, '%.18e', delimiter=' ')

					# calculate the cost
					new_cost = calc_cost()

					if new_cost < cost:
						cost = new_cost
						break

					stepsizeH = stepsizeH/2
					if stepsizeH < epsilon:
						print "H converged. RMSE: %s" % cost
						H_converged = True
						if W_converged:
							return
						else:
							break

				#increase step size for next iteration
				stepsizeH = stepsizeH*1.2
				H = Hnew

			else:
				os.system("hadoop jar " + streaming_jar + " -input " + input_file + " -output proj/output/ -mapper 'nonsparseupdate-mapper.py isForW' -reducer 'nonsparseupdate-reducer.py isForW'  -file nonsparseupdate-mapper.py -file nonsparseupdate-reducer.py  -cacheFile proj/input/w.arr#w.arr -cacheFile proj/input/h.arr#h.arr")

				# save dW
				os.system("hadoop fs -cat proj/output/part* > part-00000")

				hFile = open ( 'part-00000' , 'r')
				for line in hFile:
					data = line.split('\t', 1)
					index, vector = data
					vector = vector.split(',')
					H[:,index] = vector

				# clean up
				os.system("rm part-00000")
				os.system("hadoop fs -rm -r proj/output/")

				# display current cost
				np.savetxt('hnew.arr', H, '%.18e', delimiter=' ')
				cost = calc_cost()

				# renormalize
				norms = np.sqrt(sum(np.square(H.transpose()))).reshape(rdim,1)
				H = np.divide(H,np.dot(norms,np.ones((1,samples))))
				W = np.multiply(W,np.dot(np.ones((vdim,1)),norms.transpose()))
				np.savetxt('h.arr', H, '%.18e', delimiter=' ')
				np.savetxt('w.arr', W, '%.18e', delimiter=' ')

			os.system("hadoop fs -rm proj/input/h.arr")
			os.system("hadoop fs -put h.arr proj/input")
			os.system("hadoop fs -rm proj/input/w.arr")
			os.system("hadoop fs -put w.arr proj/input")

		if iter > 14: # When to break
			break
if __name__ == "__main__":
    main()
