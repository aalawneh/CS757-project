#!/usr/bin/python

# argument: slice_size - the size of matrix block to be sent to each reducer
# reads values from HDFS
# sends to reducer in slice_size X slice_size blocks

import sys
import re

try:
    slice_size = int(sys.argv[1])
except:
    slice_size = 1000

for line in sys.stdin:
	if not line.strip(): 
            continue
	data = re.split('\t|\:{2}', line.strip())

	if len(data) >= 3:
		row = int(data[0])-1
        col = int(data[1])-1
        val = float(data[2])

        key = '%s,%s' % (row/slice_size, col/slice_size)
        value = '%s,%s,%s' % (row, col, val)

        print '%s\t%s' % (key, value)
