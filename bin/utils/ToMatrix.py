#!/usr/bin/env python

## ToMatrix.py
## Copyright (c) 2020
## Author(s): Ranran Dai
## Contact: dairrsmu@163.com
## This script is used for putting all the digested fragments retrieved from the same read according to the unique ID of each read on one line.
## See the LICENCE file for details

"""
Script to get matrix that each line contains several fragments from the same reads
"""


import getopt
import sys
import os

def usage():
	print("This script was designed to transfer merged file to matrix")
	
	"""Usage"""
	print("Usage : python ToMatrix.py")
	print("-i/--input : <input pre-matrix file>")
	print("-o/--output : <output file>")
	print("-h/--help : <Help>")
	return

def get_args():
	"""Get arguiment"""
	try:
		opts, args = getopt.getopt(
			sys.argv[1:],
			"i:o:h",
			["INPUT=", "OUTPUT=", "help"])
	except getopt.GetoptError:
		usage()
		sys.exit(-1)
	return opts



# Read command line arguments
opts = get_args()
INPUTFile = None
OUTPUTFile = None

if len(opts) == 0:
	usage()
	sys.exit()

for opt, arg in opts:
	if opt in ("-h", "--help"):
		usage()
		sys.exit()
	elif opt in ("-i", "--input"):
		INPUTFile = arg
	elif opt in ("-o", "--output"):
		OUTPUTFile = arg
	else:
		assert False, "unhandled option"


## Print parameters
print(INPUTFile)
print(OUTPUTFile)


## To matrix
f=open(INPUTFile,'r')
F=f.read().strip()

myDict={}
for Iterm in F.split("\n"):
	Index=Iterm.split("\t")[0]
	Value=Iterm.split("\t")[1]
	if Index in myDict:
		myDict[Index].append(Value)
	else:
		myDict[Index]=[Value]


## Write out
OUTPUT = OUTPUTFile + "_raw.matrix"
fo=open(OUTPUT,"w")
for k, v in myDict.items():
	v.insert(0,k)
	S='\t'.join(v)
	fo.write( S + "\n")

