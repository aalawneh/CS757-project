#!/usr/bin/python

# calculate the gradient dH 
# dH = W'*(W*H-V);

import sys
import numpy

# Passing arguments isForW -mapper 'mapper.py arg1 arg2'  
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
				if isForW == True:					
					vVector = [0]*1682 # row
				else:
					vVector = [0]*943 # column					
					
				# here we should calculate the gradiant for user ID x
				computeGradiant(oldKey, vVector)
	
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
		HTrans = (numpy.array(H)).transpose()
		wArr = numpy.array(W)
		rowW = wArr[index,:]
		# we need H and row of W
		dW = numpy.dot(numpy.subtract(numpy.dot(rowW, H), vVector), HTrans)
		print '%s\t%s' % (index, ",".join(map(str, dW)))
	else: 
		# dH = W'*(W*H-V);
		WTrans = (numpy.array(W)).transpose()
		hArr = numpy.array(H)
		colH = hArr[:,index]
	
		# we need W and column of H
		dH = numpy.dot(WTrans, numpy.subtract(numpy.dot(W,colH), vVector))        	
		print '%s\t%s' % (index, ",".join(map(str, dH)))   
	
if __name__ == "__main__":
	wf = open ( 'w.arr' , 'r')
	W = [ map(float,line.split()) for line in wf ]

	hf = open ( 'h.arr' , 'r')
	H = [ map(float,line.split()) for line in hf ]

	main()
