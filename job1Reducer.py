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
	oldRow = None
	VRow = []
	vRow = [0]*1682
	line = read_input(sys.stdin)
	for line in sys.stdin:

		data_mapped = line.strip().split('\t')
		thisRow, value_data = data_mapped

		if thisRow:		
			if oldRow and oldRow != thisRow:
				VRow = []			
				vRow = [0]*1682
				# here we should calculate the gradiant
				computeGradiant(oldRow, vRow)
		
			oldRow = thisRow
			col, value = value_data.split(',')
			vRow[int(col)] = value

	# do not forget to compute gradiant for the last row
	if thisRow != None:
		computeGradiant(oldRow, vRow)

	# for testing .. test for the last row like 943
	if int(oldRow) == 3:
		print ""
		#print vRow
		#print W[int(oldRow)]

def computeGradiant(oldRow, vRow):
	# dH = W'*(W*H-V);

	#print W[int(oldRow)]
	index = int(oldRow)

	rowW = W[index]
	WTrans = numpy.matrix.transpose(numpy.array(W))
	colW = [row[index] for row in WTrans] 
	colH =[row[index] for row in H]		
	
	#numpy.dot(colW, )
	#print rowW
	#print "---------------"
	print vRow	
	dH = numpy.subtract(numpy.dot(rowW,colH), vRow)
	#print dH

if __name__ == "__main__":
	wf = open ( 'w.arr' , 'r')
	W = [ map(float,line.split(' ')) for line in wf ]
	#with open('w.arr') as wf:
	#    W = [[float(digit) for digit in line.split()] for line in wf]

	hf = open ( 'h.arr' , 'r')
	H = [ map(float,line.split(' ')) for line in hf ]

	main()
