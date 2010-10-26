#!/bin/sh
export LC_CTYPE=en_US.UTF-8
### obp-shpinx-up.sh
#Zoomq:091129 fixed for running stdyun host
#Zoomq:091122 creat for obp.zoomquiet.org auto buildijng Sphinx project
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DATE=`date +%y%m%d`
SVN="/usr/bin/svn"
SVNUP="$SVN up"
#RSYNC="/usr/local/rsync -avzL --delete"
#LOGFILE="/data0/logs/sync/kup-up-$DATE.log"
PATHROOT="/home/zoomq/zoomquiet.org"
LOGFILE="$PATHROOT/_logs/obp/w2py-manual_zh-$DATE.log"

echo "###::svn up & Shpinx building obp.zoomquiet.org" >> $LOGFILE
echo "###::start@" `date +%Y/%m/%d-%H:%M:%S` >> $LOGFILE
OBP="$PATHROOT/www/obp/web2py_manual_zh"
cd $OBP
pwd >> $LOGFILE
$SVNUP >> $LOGFILE 2>&1 
echo "###::reBuilding this OBP Book" >> $LOGFILE
make html >> $LOGFILE 2>&1 

echo "###::end@" `date +%Y/%m/%d-%H:%M:%S` >> $LOGFILE

exit  0

