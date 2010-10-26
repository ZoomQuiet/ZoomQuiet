#!/bin/sh
export LC_CTYPE=en_US.UTF-8
### obp-shpinx-up.sh
#Zoomq:091129 fixed for running stdyun host
#Zoomq:091122 creat for obp.zoomquiet.org auto buildijng Sphinx project
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DATE=`date +%y%m%d`
SVN="/usr/bin/svn"
SVNUP="$SVN up"
PATHROOT="/home/zoomq/zoomquiet.org"
LOGFILE="$PATHROOT/_logs/sphinx/$DATE-w2py-manual_zh.log"

echo "###::svn up & Shpinx building obp.zoomquiet.org" >> $LOGFILE
echo "###::start@" `date +%Y/%m/%d-%H:%M:%S` >> $LOGFILE
OBP="$PATHROOT/www/obp/web2py_manual_zh/source/"
cd $OBP
pwd >> $LOGFILE
$SVNUP >> $LOGFILE 2>&1 
cd ../
echo "###::reBuilding this OBP Book" >> $LOGFILE
pwd >> $LOGFILE
make html >> $LOGFILE 2>&1 

echo "###::end@" `date +%Y/%m/%d-%H:%M:%S` >> $LOGFILE
echo "#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" >> $LOGFILE
echo
echo
echo
exit  0

