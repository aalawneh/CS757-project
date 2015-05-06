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

def read_input(file):
    for line in file:
        # split the line into words
        yield line.split()

def main(separator='\t'):

	oldKey = None

	vVector = []
	if isForW == True:
		vVector = [0]*1682 # row
	else:
		vVector = [0]*943 # column

	line = read_input(sys.stdin)
	for line in sys.stdin:

		data_mapped = line.strip().split('\t')
		thisKey, value_data = data_mapped

		if thisKey:
			if oldKey and oldKey != thisKey:
				# here we should calculate the gradiant for user ID x
				computeUpdate(oldKey, vVector)

				if isForW == True:
					vVector = [0]*1682 # row
				else:
					vVector = [0]*943 # column


			oldKey = thisKey
			index, value = value_data.split(',')
			vVector[int(index)] = float(value)

	# do not forget to compute gradiant for the last row
	if thisKey != None:
		computeUpdate(oldKey, vVector)

def computeUpdate(theIndex, vVector):

	index = int(theIndex)

	if isForW == True:
		# W = W.*(V*H')./(W*H*H'+1e-9)
		rowW = W[index,:]
		wUpdate = np.divide(np.multiply(rowW,np.dot(vVector,H.transpose())),np.dot(rowW,np.dot(H,H.transpose()))+1e-9)
		print '%s\t%s' % (index, ",".join(map(str, wUpdate)))
	else:
		# H = H.*(W'*V)./(W'*W*H+1e-9)
		colH = H[:,index]
		hUpdate = np.divide(np.multiply(colH,np.dot(W.transpose(),vVector)),np.dot(np.dot(W.transpose(),W),colH)+1e-9)
		print '%s\t%s' % (index, ",".join(map(str, hUpdate)))

if __name__ == "__main__":
	wf = open ( 'w.arr' , 'r')
	W = [ map(float,line.split()) for line in wf ]
	W = np.array(W)

	hf = open ( 'h.arr' , 'r')
	H = [ map(float,line.split()) for line in hf ]
	H = np.array(H)

	main()
