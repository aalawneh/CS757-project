#!/usr/bin/python

# calculate the gradient dH 
# dH = W'*(W*H-V);

import sys
import numpy as np

# Passing arguments isForW -mapper 'mapper.py arg1 arg2'
isForW = False
if sys.argv[1] == "isForW":
	isForW = True

W = []
H = []
vdim = int(sys.argv[2])
samples = int(sys.argv[3])

def read_input(file):
    for line in file:
        # split the line into words
        yield line.split()

def main(separator='\t'):

	oldKey = None

	vVector = []
	if isForW == True:
		vVector = np.zeros(samples) # row
	else:
		vVector = np.zeros(vdim) # column
		
	line = read_input(sys.stdin)
	for line in sys.stdin:

		data_mapped = line.strip().split('\t')
		thisKey, value_data = data_mapped

		if thisKey:		
			if oldKey and oldKey != thisKey:
				# here we should calculate the gradiant for user ID x
				computeGradiant(oldKey, vVector)

				if isForW == True:					
					vVector = np.zeros(samples) # row
				else:
					vVector = np.zeros(vdim) # column
	
			oldKey = thisKey
			index, value = value_data.split(',')
			vVector[int(index)] = float(value)

	# do not forget to compute gradiant for the last row
	if thisKey != None:
		computeGradiant(oldKey, vVector)

def computeGradiant(theIndex, vVector):

	index = int(theIndex)

	if isForW == True:
		# dW = (W*H-V)*H'
		# we need H and row of W
		tmp = np.subtract(np.dot(W[index,:],H),vVector)
		tmp[np.nonzero(vVector==0)]=0
		dW = np.dot(tmp, H.transpose())
		print '%s\t%s' % (index, ",".join(map(str, dW)))
	else: 
		# dH = W'*(W*H-V);
		# we need W and column of H
		tmp = np.subtract(np.dot(W,H[:,index]), vVector)
		tmp[np.nonzero(vVector==0)]=0
		dH = np.dot(W.transpose(), tmp)
		print '%s\t%s' % (index, ",".join(map(str, dH)))   
	
if __name__ == "__main__":
	wf = open ( 'w.arr' , 'r')
	W = [ map(float,line.split()) for line in wf ]
	W = np.array(W)

	hf = open ( 'h.arr' , 'r')
	H = [ map(float,line.split()) for line in hf ]
	H = np.array(H)

	main()
