## build_in.sh
##
## Tri-3C-HTGTS_pro
## Copyright (c) 2020 
## Author(s): Ranran Dai
## Contact: dairrsmu@163.com
## This script is used for mining multi-way chromatin interactions from 3C-HTGTS data.
## See the LICENCE file for details

###########################
## Build-in shell script
###########################

## trace ERROR in shell pipes
set -o pipefail
set -o nounset

CURRENT_PATH=`dirname $0`

tmpfile1=/tmp/HTGT1.$$
tmpfile2=/tmp/HTGT2.$$
tmpmkfile=/tmp/HTGTmk.$$
trap "rm -f $tmpfile1 $tmpfile2 $tmpmkfile" 0 1 2 3

abspath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}

config_filter()
{
sed -e 's/#.*//' | egrep '^[ \t]*[a-zA-Z_][a-zA-Z0-9_]*[ \t]*:?=' | sed -e 's/[ \t]*:=[ \t]*/ :=/' -e 's/[ \t][^:]*=[ \t]*/ =/' -e 's/\([^ \t]*\)=/\1 =/' -e 's/ *$//g' | sort -u -k 1b,1
}

read_config()
{
    local conf=$1
    cat $conf > $tmpmkfile
    echo "_dummy_target_:" >> $tmpmkfile
    make -f $tmpmkfile -p -n | config_filter > $tmpfile1
    cat $conf | config_filter > $tmpfile2

    eval "$(join $tmpfile1 $tmpfile2 | awk -F' =' '{printf("%s=\"%s\"; export %s;\n", $1, $2, $1)}')"

}


## Part 2
die() 
{
    echo "Exit: $@" 1>&2
    exit 1
}


## part 3 : read config file
## load Tri-3C-HTGTS config
if [ ! -z "$CONF" ]; then
    CONF=`abspath $CONF`
    if [ -e "$CONF" ]; then
        read_config $CONF
    else
        echo "Error - Tri-3CHTGTS config file '$CONF' not found"
        exit
    fi
fi
