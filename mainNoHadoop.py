#!/usr/bin/env python

import sys
import os

try:
    import numpy as np
except:
    print "This implementation requires the numpy module."
    exit(0)

if len(sys.argv) < 7:
	print "Usage: ./main.py input_file rows columns inside_dimension sparseness_W sparseness_H"
	return

# different input files
input_file = sys.argv[1]

def projfunc(s, k1, k2):
	# this will be a mapreduce job later
	n = len(s)

	v = s + (k1-sum(s))/n

	zerocoeff = []

	while True:
		mid = np.ones(n)*k1/(n-len(zerocoeff))
		mid[zerocoeff] = 0
		w = v - mid
		a = np.sum(np.square(w))
		b = 2*np.dot(w,v)
		c = np.sum(np.square(v))-k2
		alphap = (-b+np.real(np.sqrt(complex(b**2-4*a*c))))/(2*a)
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
	os.system("cat " + input_file + " | ./cost-mapper.py 1000 | sort -n | ./cost-reducer.py > cost_output.dat ");
	
	count = 0
	sse = 0
	costFile = open ( 'cost_output.dat' , 'r')
	for line in costFile:
		data = line.split('\t')
		count += int(data[0])
		sse += float(data[1])
	
	rmse = np.sqrt(sse/count)
	print "Current RMSE: %s" % rmse
	os.system("rm -f cost_output.dat")
	return rmse


def main():
	# internal dimension
	rdim = int(sys.argv[4])
	# The number of rows in V
	vdim = int(sys.argv[2])
	# The number of columns in V
	samples = int(sys.argv[3])

	reducer_args = " %d %d " % (vdim, samples)

	# sparseness constraints for W and H
	sW = float(sys.argv[5])
	sH = float(sys.argv[6])
	# epsilon value for convergence detection
	epsilon = 1e-5
	W_converged = False
	H_converged = False

	# Create initial matrices: 
	# vdim-by-rdim matrix of normally distributed random numbers.
	W = abs(np.random.randn(vdim,rdim))
	# rdim-by-samples matrix of normally distributed random numbers.
	H = abs(np.random.randn(rdim,samples))
	H = np.divide(H,np.dot(np.sqrt(np.sum(np.square(H),1)).reshape(rdim,1),np.ones((1,samples))))

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
	
	cost = calc_cost()

	# Initial stepsizes
	stepsizeW = 1.0
	stepsizeH = 1.0

	# Start iteration
	iter = 0

	while True:
		iter += 1
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
				os.system("cat " + input_file + " |  ./gradient-mapper.py isForW | sort -n | ./gradient-reducer.py isForW " + reducer_args + " > gradient-output.dat")

				# save dW
				os.system("mv gradient-output.dat dW.arr")

				dW = np.zeros((vdim,rdim))
				wFile = open ( 'dW.arr' , 'r')
				for line in wFile:
					data = line.split('\t', 1)
					index, vector = data
					vector = vector.split(',')
					dW[index,:] = vector

				# clean up
				os.system("rm -f gradient-output.dat")

				while True:
					# Update W --> Wnew = W- stepsize * dW
					Wnew = np.subtract(W, stepsizeW*dW)

					# do the projection
					norms = np.sqrt(np.sum(np.square(Wnew),0))
					for i in range(0,rdim):
						Wnew[:,i] = projfunc(Wnew[:,i],L1a*norms[i],norms[i]**2)

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
				if W_converged == False:
					W = Wnew

			else:
				os.system("cat " + input_file + " | ./nonsparseupdate-mapper.py isForW | sort -n | ./nonsparseupdate-reducer.py isForW > nonsparseupdate.dat")

				# save dW

				wFile = open ( 'nonsparseupdate,dat' , 'r')
				for line in wFile:
					data = line.split('\t', 1)
					index, vector = data
					vector = vector.split(',')
					W[index,:] = vector

				# clean up
				os.system("rm -f nonsparseupdate.dat")

				# display current cost
				np.savetxt('wnew.arr', W, '%.18e', delimiter=' ')
				cost = calc_cost()

			np.savetxt('w.arr', W, '%.18e', delimiter=' ')



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
				os.system("cat " + input_file + " | ./gradient-mapper.py isForH | sort -n | ./gradient-reducer.py isForH" + reducer_args + " > gradient.dat")

				# save dH

				os.system("mv gradient.dat dH.arr")

				dH = np.zeros((rdim,samples))
				wFile = open ( 'dH.arr' , 'r')
				for line in wFile:
					data = line.split('\t', 1)
					index, vector = data
					vector = vector.split(',')
					dH[:,index] = vector

				# clean up
				os.system("rm -f gradient.dat")

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
				if H_converged == False:
					H = Hnew

			else:
				os.system("cat " + input_file + "| ./nonsparseupdate-mapper.py isForH | sort -n | ./nonsparseupdate-reducer.py isForH > nonsparseupdate.dat")

				# save dW


				hFile = open ( 'nonsparseupdate.dat' , 'r')
				for line in hFile:
					data = line.split('\t', 1)
					index, vector = data
					vector = vector.split(',')
					H[:,index] = vector

				# clean up
				os.system("rm -f nonsparseupdate.dat")

				# display current cost
				np.savetxt('hnew.arr', H, '%.18e', delimiter=' ')
				cost = calc_cost()

				# renormalize
				norms = np.sqrt(sum(np.square(H.transpose()))).reshape(rdim,1)
				H = np.divide(H,np.dot(norms,np.ones((1,samples))))
				W = np.multiply(W,np.dot(np.ones((vdim,1)),norms.transpose()))
				np.savetxt('w.arr', W, '%.18e', delimiter=' ')

			np.savetxt('h.arr', H, '%.18e', delimiter=' ')

		if iter > 49: # When to break
			break
if __name__ == "__main__":
    main()
