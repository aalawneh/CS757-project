#!/usr/bin/env python

import sys
import os

try:
    import numpy as np
except:
    print "This implementation requires the numpy module."
    exit(0)

#this will differ by environment
#streaming_jar = "/usr/local/Cellar/hadoop/2.6.0/libexec/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar"
#streaming_jar = "/usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.1.1.jar"
#hydra
streaming_jar = "/apps/hadoop-2/share/hadoop/tools/lib/hadoop-streaming-2.4.1.jar -D mapred.reduce.tasks=5"


def calc_cost():
	os.system("hadoop fs -put -Ddfs.block.size=8388608 V.arr test/input")
	os.system("hadoop fs -put hnew.arr test/input")
	os.system("hadoop fs -put wnew.arr test/input")
	os.system("hadoop jar " + streaming_jar + " -input test/input/V.arr -output test/output/ -mapper 'cost-mapper.py 1000' -reducer 'cost-reducer.py'  -file cost-mapper.py -file cost-reducer.py  -cacheFile test/input/wnew.arr#wnew.arr -cacheFile test/input/hnew.arr#hnew.arr")

	os.system("hadoop fs -cat proj/output/part* > part-00000")
	os.system("hadoop fs -rm -r proj/output")
	os.system("hadoop fs -rm proj/input/*")

	count = 0
	sse = 0
	costFile = open ( 'part-00000' , 'r')
	for line in costFile:
		data = line.split('\t')
		count += int(data[0])
		sse += float(data[1])

	rmse = np.sqrt(sse/count)
	print "Current RMSE: %s" % rmse
	os.system("rm part-00000")
	return rmse

os.system("mv w1.arr wnew.arr")
os.system("mv h1.arr hnew.arr")
os.system("mv r1.test V.arr")
calc_cost()
os.system("mv wnew.arr w1.arr")
os.system("mv hnew.arr h1.arr")
os.system("mv V.arr r1.test")

os.system("mv w2.arr wnew.arr")
os.system("mv h2.arr hnew.arr")
os.system("mv r2.test V.arr")
calc_cost()
os.system("mv wnew.arr w2.arr")
os.system("mv hnew.arr h2.arr")
os.system("mv V.arr r2.test")

os.system("mv w3.arr wnew.arr")
os.system("mv h3.arr hnew.arr")
os.system("mv r3.test V.arr")
calc_cost()
os.system("mv wnew.arr w3.arr")
os.system("mv hnew.arr h3.arr")
os.system("mv V.arr r3.test")

os.system("mv w4.arr wnew.arr")
os.system("mv h4.arr hnew.arr")
os.system("mv r4.test V.arr")
calc_cost()
os.system("mv wnew.arr w4.arr")
os.system("mv hnew.arr h4.arr")
os.system("mv V.arr r4.test")

os.system("mv w5.arr wnew.arr")
os.system("mv h5.arr hnew.arr")
os.system("mv r5.test V.arr")
calc_cost()
os.system("mv wnew.arr w5.arr")
os.system("mv hnew.arr h5.arr")
os.system("mv V.arr r5.test")
