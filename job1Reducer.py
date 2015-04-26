#!/usr/bin/python

# calculate the gradient dH 
# dH = W'*(W*H-V);

import sys
import numpy

# Passing arguments isForW -mapper 'count_mapper.py arg1 arg2'  
# arg1 = sys.argv[1]
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
		# vRow
		vVector = [0]*1682 
	else:
		# vColumn		
		vVector = [0]*943
	line = read_input(sys.stdin)
	for line in sys.stdin:

		data_mapped = line.strip().split('\t')
		thisKey, value_data = data_mapped

		if thisKey:					 
			if oldKey and oldKey != thisKey:
				vVector = []
				if isForW == True:
					vVector = [0]*943 # row
				else:
					vVector = [0]*1682  # column
				# here we should calculate the gradiant for user ID x
				computeGradiant(oldKey, vVector)
	
			oldKey = thisKey
			index, value = value_data.split(',')
			vVector[int(index)] = float(value)

	# do not forget to compute gradiant for the last row
	if thisKey != None:
		computeGradiant(oldKey, vVector)

	# for testing .. test for the last colum like 943
	if int(oldKey) == 3:
		print ""
		#print vRow

def computeGradiant(theIndex, vVector):

	index = int(theIndex)

	if isForW == True:
		# dH = W'*(W*H-V);
		WTrans = (numpy.matrix(W)).transpose()
		hArr = numpy.array(H)
		colH = hArr[:,index]
	
		# dH for column(index)
		dH = numpy.dot(WTrans, numpy.subtract(numpy.dot(W,colH), vVector))
		print numpy.subtract(numpy.dot(W,colH), vVector)
	else:
		# dW = (W*H-V)*H'
		#HTrans = (numpy.matrix(H)).transpose()
		#wArr = numpy.array(W)
		#rowW = wArr[index,:]

		# dH for row(index)
		#dW = numpy.dot(numpy.subtract(numpy.dot(W,rowW), vVector), HTrans)
		print ""
	
if __name__ == "__main__":
	wf = open ( 'w.arr' , 'r')
	W = [ map(float,line.split()) for line in wf ]

	hf = open ( 'h.arr' , 'r')
	H = [ map(float,line.split()) for line in hf ]

	main()
