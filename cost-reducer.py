#!/usr/bin/python

# compares incoming actual values of V to the hypothetical values calculated from W and H
# accumulates and emits number of examples seen so far and the sum of squared error (1 line of output from each reducer)

import sys
import numpy as np

W = []
H = []

def main():
    n = 0
    sse = 0.0

    for line in sys.stdin:
        line = line.strip()
        key,value = line.split('\t')
        row,col,val = value.split(',')
        row = int(row)
        col = int(col)
        val = float(val)
        n = n+1
        sse = sse + (val - (np.dot(W[row,:], H[:,col])*5.0))**2
        
    print '%s\t%s' % (n, sse)

	
if __name__ == "__main__":
    # later we will be passed bits of W and H from the mapper
    wf = open ( 'wnew.arr' , 'r')
    W = [ map(float,line.split(' ')) for line in wf ]
    W = np.array(W)

    hf = open ( 'hnew.arr' , 'r')
    H = [ map(float,line.split(' ')) for line in hf ]
    H = np.array(H)

    main()
