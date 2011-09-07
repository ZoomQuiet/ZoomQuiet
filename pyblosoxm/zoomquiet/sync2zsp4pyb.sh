#!/bin/sh
#export LC_CTYPE=en_US.UTF-8
###Changelog::
#==================================================================== abt. define
VER="sync2zsp4pyb.sh v11.09.7"
DATE=`date "+%y%m%d"`

PY=$( which python)
SYNC=$( which rsync)
#==================================================================== abt. path
PYB="~/zq.pyblosxom/zoomquiet/"
ZSP="zeus:~/zoomquiet.org/blog/"
#==================================================================== abt. action
echo "###::run@" `date +"%Y/%m/%d %H:%M:%S"` 

cd $PYB
echo ">>>   $VER publishing pyblosxom to ZSP's stdyun"
    echo ">>>   fixed all category's idx '"
$PY plugins/cp4idx2category.py _static

    echo ">>>   rsync up to zoomquiet.org '"
$SYNC -avzP4 --delete --safe-links -e ssh ./* $ZSP

echo "###::end@" `date +"%Y/%m/%d %H:%M:%S"` 
#==================================================================== end shell script
exit  0

