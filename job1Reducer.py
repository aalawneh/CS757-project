#!/usr/bin/python

# calculate the gradient dH 
# dH = W'*(W*H-V);

import sys
import numpy

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
				computeGradiant(oldRow)
		
			oldRow = thisRow
			col, value = value_data.split(',')
			vRow[int(col)] = value

	# do not forget to compute gradiant for the last row
	if thisRow != None:
		computeGradiant(oldRow)

	# for testing .. test for the last row like 943
	if int(oldRow) == 3:
		print vRow
		#print W[int(oldRow)]

def computeGradiant(movies):
	wf = open ( 'w.arr' , 'r')
	W = [ map(float,line.split(' ')) for line in wf ]
	#with open('w.arr') as wf:
	#    W = [[float(digit) for digit in line.split()] for line in wf]

	hf = open ( 'h.arr' , 'r')
	H = [ map(float,line.split(' ')) for line in hf ]

if __name__ == "__main__":
	main()
