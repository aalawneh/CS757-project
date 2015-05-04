#!/usr/bin/python

import sys
import numpy as np
import re

ratings_file = sys.argv[1]
user_id = int(sys.argv[2])
W=[]
H=[]
v=[]
m=[]

def main():
	v_approx = np.dot(W[user_id,:],H)*2+3
	v_approx[np.nonzero(v)] = 0 # remove movies they've already rated

	fav = np.argsort(-v)[:8]
	print "Highest-Rated movies:\n-----"
	for f in fav:
		print m[f]
	best = np.argsort(-v_approx)[:8]
	print "\nRecommended movies\n-----"
	for b in best:
		print m[b]

if __name__ == "__main__":
	wf = open ( 'w.arr' , 'r')
	W = [ map(float,line.split()) for line in wf ]
	W = np.array(W)

	hf = open ( 'h.arr' , 'r')
	H = [ map(float,line.split()) for line in hf ]
	H = np.array(H)

	v = np.zeros(len(H[1,:]))
	vf = open(ratings_file, 'r')

	for line in vf:
		data = re.split('\t|\:{2}', line.strip())

		if len(data) >= 3:
			row = int(data[0])
			if row == user_id:
				col = int(data[1])-1
				v[col] = float(data[2])

	m = [None]*len(H[1,:])
	mf = open('u.item', 'r')

	for line in mf:
		data = line.split('|')

		col = int(data[0])-1
		m[col] = data[1]
	main()
