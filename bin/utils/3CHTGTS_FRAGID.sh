#!/bin/bash

## Find bait fragment id for Tri-3CHTGTS

## 3CHTGTS_FRAGID.sh
## Copyright (c) 2020 
## Author(s): Ranran Dai
## Contact:
## This software is distributed without any guarantee under the terms of the BSD-3 licence.
## See the LICENCE file for details

## Description:
## 3CHTGTS_FRAGID.sh for 3C-HTGTS triplet-interaction mining ;
## 


SOFT="3CHTGTS_FRAGID.sh"
VERSION="1.0.0"

function usage {
        echo -e "Usage : $SOFT -c CONFIG [-h] [-v]"
        echo -e "Usage option -h|--help for more information"
}

######## Help function ########
function help {
        usage;
        echo
        echo "$SOFT $VERSION"
        echo "--------------"
        echo "OPTIONS"
        echo
        echo -e "\t -c|--config CONFIG : config file of 3CHTGTS;"
        echo -e "\t [-h|--help]: help"
        echo -e "\t [-v|--version]: version"
        echo
        echo -e "Example:"
        echo -e "\t 3CHTGTS_FRAGID.sh -c Config.txt"
        exit;
}


function version {
        echo -e "$SOFT version $VERSION"
        exit;
}

#####################
## Inputs
#####################
if [ $# -lt 1 ]
then
    usage
    exit 1
fi


while [[ $# -gt 0 ]]
do
        key="$1"
#       echo -e "key:"$key
        case $key in
                --config|-c) CONFIG=$2; shift;;
                --version|-v) version ; exit 2;;
                --help|-h) help; exit 2 ;;
                *)
                echo option \'$1\' not understood!
                echo use 3CHTGTS_FRAGID.sh --help to see correct usage!
                exit 2
                ;;
                esac
        shift
done

echo "CONFIG FILE:"$CONFIG

Reduced_genome_Fa=`grep Reduced_genome_Fa $CONFIG | tr -d "" | cut -d "=" -f 2`
NestPrimer=`grep NestPrimer $CONFIG | tr -d "" | cut -d "=" -f 2`
FRAGID=`grep FRAGID $CONFIG | tr -d "" | cut -d "=" -f 2`

BAITFID=''
BAITFID=`grep -B 1 $NestPrimer $Reduced_genome_Fa | head -n 1| awk -F "[_@]" '{OFS="_"}{print $2,$3}'`
BAITFID=`echo $BAITFID |awk -F "\t" '{OFS="\t"}{print "HIC_"$1}'`
BaitCoordinate=`grep -w $BAITFID $FRAGID | head -n 1 |awk -F "\t" '{OFS="\t"}{print $1,$2,$3}'`

if [[ $BAITFID == '' ]]
then
	echo -e "> NestPrimer\n"$NestPrimer > NP.fa
	seqtk seq -r NP.fa > NP_rev.fa
	NestPrimer=`tail -n 1 NP_rev.fa`
	BAITFID=`grep -B 1 $NestPrimer $Reduced_genome_Fa | head -n 1| awk -F "[_@]" '{OFS="_"}{print $2,$3}'`
	BAITFID=`echo $BAITFID |awk -F "\t" '{OFS="\t"}{print "HIC_"$1}'`
	BaitCoordinate=`grep -w $BAITFID $FRAGID | head -n 1 |awk -F "\t" '{OFS="\t"}{print $1,$2,$3}'`
	rm NP_rev.fa NP.fa
fi

echo "Bait Enzyme Fragment ID:" $BAITFID
echo "Chromosome coordinates of bait:"$BaitCoordinate
