#!/usr/bin/env python

# AfterMatrix2bedpe.py
# Copyleft 2015 Institut Curie
# Author(s):
# Contact: nicolas.servant@curie.fr
# This software is distributed without any guarantee under the terms of the
# GNU General
# Public License, either Version 2, June 1991 or Version 3, June 2007.

"""
Script to transfer triplet interactors matrixs to bedpe file for igv
"""

## function for bedpe file; enzyme fragment counting
def FragMat2bedpe(matrixfile):
    # read chrom size file
    infile = open(matrixfile)
    outDict = {}
    Mat = infile.read().strip()
    for Iterm in Mat.split("\n"):
        first = Iterm.split("\t")[1].split("|")[1]
        second = Iterm.split("\t")[2].split("|")[1]
        if int(first.split("-")[1]) < int(second.split("-")[1]):
            Index = first + "|" + second
        else:
            Index = second + "|" + first
        if Index in outDict:
            outDict[Index] += 1
        else:
            outDict[Index] = 1
    # dict to matrix
    outList = []
    for k,v in outDict.items():
        Loci = k.replace(":","|").replace("-","|").split("|")
        Loci.append(str(v))
        outList.append(Loci)
    return outList

## function for bedpe file; binsize counting
def BinMat2bedpe(matrixfile,binsize):
    # read chrom size file
    infile = open(matrixfile)
    outDict = {}
    Mat = infile.read().strip()
    line = 1
    for Iterm in Mat.split("\n"):
        # fc: first fragment chromosome; fs: first fragment start; fe: first fragment end; fm: median site of first fragment; fmb: bin median id of first fragment
        fc = Iterm.split("\t")[1].split("|")[1].split(":")[0]
        fs = Iterm.split("\t")[1].split("|")[1].split(":")[1].split("-")[0]
        fe = Iterm.split("\t")[1].split("|")[1].split(":")[1].split("-")[1]
        fm = (int(fs) + int(fe)) // 2
        fmb = ((int(fm) // int(binsize)) + 1) * int(binsize)
        # sc: second fragment chromosome; ss: second fragment start; se: second fragment end; sm: median site of second fragment
        sc = Iterm.split("\t")[2].split("|")[1].split(":")[0]
        ss = Iterm.split("\t")[2].split("|")[1].split(":")[1].split("-")[0]
        se = Iterm.split("\t")[2].split("|")[1].split(":")[1].split("-")[1]
        sm = (int(ss) + int(se)) // 2
        smb = (int(sm) // int(binsize) + 1) * int(binsize)
        # keep smb == fmb and smaller one lie in first
        if  fmb <= smb:
            Index = str(fc) + ":" + str(fmb) + "|" + str(sc) + ":" + str(smb)
        else:
            Index = str(sc) + ":" + str(smb) + "|" + str(fc) + ":" + str(fmb)
        if Index in outDict:
            outDict[Index] += 1
        else:
            outDict[Index] = 1
        line += 1
    print("line:",line)
    # dict to matrix
    outList = []
    for k,v in outDict.items():
        #print "k:",k
        LS = k.replace(":","|").split("|")
        #print "LS:",LS
        Loci = [LS[0], str(int(LS[1]) - int(binsize) // 2), str(int(LS[1]) + int(binsize) // 2), LS[2], str(int(LS[3]) - int(binsize) // 2), str(int(LS[3]) + int(binsize) // 2), str(v)]
        outList.append(Loci)
    return outList

## function for command parrameters
def main(argv):
    global matrixfile
    global outputdir
    global binsize
    try:
        opts, args = getopt.getopt(argv,"h:i:o:b:",["matrixfile=","outputdir=","binsize="])
    except getopt.GetoptError:
        print('3CHTGTSMatrix2bedpe.py -i <matrixfile> -o <outputdir> [-b <binsize>]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('3CHTGTSMatrix2bedpe.py -i <matrixfile> -o <outputdir> [-b <binsize>]')
            sys.exit()
        elif opt in ("-i", "--matrixfile"):
            matrixfile = arg
        elif opt in ("-o", "--outputdir"):
            outputdir = arg
        elif opt in ("-b", "--binsize"):
            binsize = arg
        else:
            print('3CHTGTSMatrix2bedpe.py -i <matrixfile> -o <outputdir> [-b <binsize>]')
            sys.exit(3)


## main function
import os, sys, getopt

matrixfile = ''
outputdir = ''
binsize = 1

if __name__ == "__main__":
    main(sys.argv[1:])

if matrixfile == '' and outputdir == '':
    print('ERROR in parramaters:\n\t please cheack by : 3CHTGTSMatrix2bedpe.py -h')
    sys.exit(1)

print('matrix file is :', matrixfile)
print('output file is :', outputdir)
print('binsize is :', binsize)


OutList = []
Outmatrix_name = ''
fnam = os.path.basename(matrixfile).split(".")[0]
## only return one file: Enzyme Fragment loop or bin based loop
if int(binsize) > 10000:
    OutList = BinMat2bedpe(matrixfile, binsize)
    Outmatrix_name = outputdir + "/" + fnam + "_bin" + str(binsize) + ".bedpe"
else:
    OutList = FragMat2bedpe(matrixfile)
    Outmatrix_name = outputdir + "/" + fnam + "_Fragment.bedpe"

# write out Bin_Bed and Bin_Mat
print(OutList[1])
m_fo = open(Outmatrix_name, "w")
for LI in OutList:
    s = '\t'.join(LI)
    m_fo.write( s + "\n" )


 
