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
	oldColumn = None
	VRow = []
	vRow = [0]*1682
	VColumn = []
	vColumn = [0]*943
	line = read_input(sys.stdin)
	if isForW == True:
		for line in sys.stdin:

			data_mapped = line.strip().split('\t')
			thisColumn, value_data = data_mapped

			if thisColumn:		
				if oldColumn and oldColumn != thisColumn:
					VColumn = []
					vColumn = [0]*943
					# here we should calculate the gradiant for user ID x
					computeGradiant(oldColumn, vColumn)
		
				oldColumn = thisColumn
				row, value = value_data.split(',')
				vColumn[int(row)] = float(value)

		# do not forget to compute gradiant for the last row
		if thisColumn != None:
			computeGradiant(oldColumn, vColumn)

		# for testing .. test for the last row like 943
		if int(oldColumn) == 3:
			print ""
			#print vRow

	else:
		for line in sys.stdin:

			data_mapped = line.strip().split('\t')
			thisRow, value_data = data_mapped

			if thisRow:		
				if oldRow and oldRow != thisRow:
					VRow = []			
					vRow = [0]*1682
					# here we should calculate the gradiant for user ID x
					computeGradiant(oldRow, vRow)
		
				oldRow = thisRow
				col, value = value_data.split(',')
				vRow[int(col)] = float(value)

		# do not forget to compute gradiant for the last row
		if thisRow != None:
			computeGradiant(oldRow, vRow)


def computeGradiant(theIndex, vVector):
	if isForW == True:
		# dH = W'*(W*H-V);

		index = int(theIndex)

		WTrans = (numpy.matrix(W)).transpose()
		hArr = numpy.array(H)
		colH = hArr[:,index]
	
		# dH for column(index)
        	dH = numpy.dot(WTrans, numpy.subtract(numpy.dot(W,colH), vVector))
		print dH
	else:
		print ""
	
if __name__ == "__main__":
	wf = open ( 'w.arr' , 'r')
	W = [ map(float,line.split()) for line in wf ]

	hf = open ( 'h.arr' , 'r')
	H = [ map(float,line.split()) for line in hf ]

	main()
