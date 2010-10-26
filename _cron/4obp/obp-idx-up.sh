#!/bin/sh
#export LC_CTYPE=en_US.UTF-8
### obp-idx-up.sh
#Zoomq:091129 creat for obp.zoomquiet.org auto buildijng site mapping
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DATE=`date +%y%m%d`
SVN="/usr/bin/svn"
SVNUP="$SVN up"
PATHROOT="/home/zoomq/zoomquiet.org"
LOGFILE="$PATHROOT/_logs/dotmap/$DATE-mapping-up.log"
DOTMAP='./dot-gen-html.py dot res/index.tpl obp-zq-idx.dot "O.B.P_图书日构建发布中心_资源地图" index.html'

echo "###::svn up & Graphiviz building obp.zoomquiet.org mapping" >> $LOGFILE
echo "###::start@" `date +%Y/%m/%d-%H:%M:%S` >> $LOGFILE
OBP="$PATHROOT/www/map"
cd $OBP
$SVNUP >> $LOGFILE 2>&1
 
chmod +x dot-gen-html.py

pwd >> $LOGFILE
echo "$DOTMAP"  >> $LOGFILE 2>&1 
$DOTMAP >> $LOGFILE 2>&1 

echo "###::end@" `date +%Y/%m/%d-%H:%M:%S` >> $LOGFILE

exit  0

