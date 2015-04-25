#!/usr/bin/python

import sys

oldRow = None
VRow = []
vRow = [0]*1682

# calculate the gradient dH 
# dH = W'*(W*H-V);

wf = open ( 'w.arr' , 'r')
W = [ map(float,line.split(' ')) for line in wf ]

hf = open ( 'h.arr' , 'r')
H = [ map(float,line.split(' ')) for line in hf ]

for line in sys.stdin:

	data_mapped = line.strip().split('\t')
	thisRow, value_data = data_mapped

	if thisRow:		
		if oldRow and oldRow != thisRow:
			VRow = []			
			vRow = [0]*1682
		
		oldRow = thisRow
		col, value = value_data.split(',')
		vRow[int(col)] = value

# for testing .. test for the last row like 943
if int(oldRow) == 3:
	print vRow

