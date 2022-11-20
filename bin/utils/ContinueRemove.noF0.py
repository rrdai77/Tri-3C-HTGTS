#! /usr/bin/env python

import getopt
import sys
import os
import re

## functions
# usage function
def usage():
        print("remove continue fragment in pre-matrix from 3C-HTGTSMutimatix.sh")

        """Usage"""
        print("Usage : python ContinusRemove.py")
        print("-i/--input : <input matrix file>")
        print("-o/--output : <output file basename>")
        print("-b/--baiteFID :  <enzyme fragment ID : example: chr12_277>")
        print("-h/--help : <Help>")
        return

# command parameter function
def get_args():
        """Get argument"""
        try:
                opts, args = getopt.getopt(
                        sys.argv[1:],
                        "i:o:b:h",
                        ["INPUT=","BAITEFID=","OUTPUT=","help"])
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
        elif opt in ("-b", "--baiteFID"):
                BAITEFID = arg
        else:
                assert False, "unhandled option"

## MOD2 : multiple fragment, just cis fragments considered

## function Ranges
#### detect ranges of a number list after duplication remove
#### example : 
## Ranges([2, 3, 4, 7, 8, 9, 15])
## [(2, 4), (7, 9), (15, 15)]
## Result [star, end)

def Ranges(nums):
	nums = sorted(set(nums))
	gaps = [[s, e] for s, e in zip(nums, nums[1:]) if s+1 < e]
	edges = iter(nums[:1] + sum(gaps, []) + nums[-1:])
	return [[s, e] for s, e in zip(edges, edges)]
#	edges = sorted(set(edges))
#	L = [[s, e] for s, e in zip(edges, edges[1:]) if s+1 < e]
#	return L


def Frag2Dict(List):	
	Dict = {}
	for index, item in enumerate(List):
		Key = index
		Value = item.split("|")[0].split("_")[1:] 
		Dict[Key] = Value
	return Dict

def Filter(RList, BAITEFID):
	## baiteID
	pa = "HiC_" + BAITEFID + "|"
	baiteID = int(BAITEFID.split("_")[1])
	## transfer fragment list to diction with list index as key
	MyDict = Frag2Dict(RList[1:])
	## Fragment ID list for rang finding
	ID_List = [int(MyDict[key][1]) for key in MyDict]
	##  slected site list; 
	## if continus contain baiteID, return BaiteID else return mixnum FragID
	SL = []
	for iterm in Ranges(ID_List):
		if iterm[0] <= baiteID and iterm[1] >= baiteID:
			SL.append(baiteID)
		else:
			SL.append(iterm[0])
	## SL_key
	SK_Key = [int(key) + 1 for value in SL for key, VALUE in MyDict.items() if int(VALUE[1]) == int(value)]
	## return new List
	NewList = [RList[0]]
	for index in SK_Key:
		NewList.append(RList[index])
	return NewList

################
## main function
################

## print parameters
print(INPUTFile)
print(OUTPUTFile)
print(BAITEFID)



## read Matrix and remove reads that cis fragments length less than 3
f = open(INPUTFile, "r")
F = f.read().strip()

BAITECHR = BAITEFID.split("_")[0]

MAF1 = []
for L in F.split("\n"):
	## read ID
	LN = [L.split("\t")[0]]
	## F0 is not located in Baite enzyme fragment;because short DNA fragment length
	FL = L.split("\t")[1:]
	pa = "HiC_" + BAITEFID + "|"
	## add Baite fragmentID to the first element
	LN.append(pa)
	#FL.insert(0, pa)
	pattern1 = BAITEFID + "\\|"
	## remove trans enzyme fragment and baite fragment that not in F0
	for iterm in FL:
		## remove trans
		pattern = "_" + BAITECHR + "_"
		math1 = re.search(pattern, iterm)
		
		## remove baite fragment id
		math2 = re.search(pattern1, iterm)
		if math1 and math2 is None :
			LN.append(iterm)
	if len(LN) >= 3:
		MAF1.append(LN)

## Filter continus fragments in read
MAF2 = []
for L1 in MAF1:
	F=L1[2:]
	K=[]
	V=[]
	for S in F:
		key=S.split("|")[1]+"|"+S.split("|")[2]	
		K.append(key)
		value=S.split("|")[0]
		V.append(value)
	A=dict(zip(K,V))
	func = lambda z: dict([(x, y) for y, x in z.items()])
	B=func(A)
	L2=[]
	for key,value in B.items():
		P=key+"|"+value
		L2.append(P)
	L3=L1[:2]
	L4= L3 + L2
		
	L4_Filter = Filter(L4, BAITEFID)
	if len(L4_Filter) >= 3:
		MAF2.append(L4_Filter)


## resort , keep the baite fragment in the first coln.and others keep old sequence
MAF3 = []
pattern1 = BAITEFID + "\\|"

for L2 in MAF2:
	## read ID
	LN2 = [L2[0]]
	for i in list(range(1,len(L2))):
		iterm = L2[i]
		math3 = re.search(pattern1, iterm)
		if math3:
			LN2.append(L2[i])
			LN2 = LN2 + L2[1:i] + L2[i+1:]
			MAF3.append(LN2)
			break



## Wirte out
OUTFILE = OUTPUTFile + '_continues_removed.matrix'
fo = open(OUTFILE, "w")
for LO in MAF3:
	LOSTR='\t'.join(LO) + "\n"
	fo.write(LOSTR)


