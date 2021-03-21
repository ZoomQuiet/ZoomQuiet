#!/bin/sh
# base incoming hooks API auto deploy new content from gitcafe
#
#  210321 base native timestamp
#  160412 working
#=========================================================== var defines
VER="ffsplit.sh v.210321"
DATE=`date "+%y%m%d"`
#NOW=$(date +"%Y-%m-%d")
#GIT=$( which git)
#=========================================================== path defines
#LOGF="/opt/logs/cron/$DATE-git-cn-pycon.log"
#RESPATH="/opt/www/PyConChina.github.io"
#=========================================================== action defines
START=$(date +%s)

if [ -z $1 ] || [ -z $2 ]; then
   echo "Usage:$0 START DURATION exp.NAME inVideo"
   echo "   eg. $0 10 80 exp2.mp4 foo.avi"
   echo "   eg. $0 00:00:10 00:01:20 exp2.mp4 foo.avi"
   exit
fi

echo "cut from $1 to $2"
#date --date '2017-08-17 04:00:01' +%s    # "1502938801"

CUTIN=$(date -u -d "$1" +"%s")
CUTOUT=$(date -u -d "$2" +"%s")

#CUTIN=$((date --date "1974-11-11 $1" +%s))
#CUTOUT=$((date --date "1974-11-11 $2" +%s))
#echo "cut as $CUTIN to $CUTOUT"
CUTDUE=$(date -u -d "0 $CUTOUT sec - $CUTIN sec" +"%H:%M:%S")
#echo "long $CUTDUE"

#echo "ffmpeg -i $4 -ss $1 -t $CUTDUE $3"
#ffmpeg -i "$4" -ss $1 -t $2 $3
ffmpeg -i "$4" -ss $1 -t $CUTDUE -vf scale=iw/2:-1 -sws_flags fast_bilinear $3

ALLDO=$(date +%s)
DUE=$(($ALLDO - $START))
echo "\n transform by FFmpeg"
echo "\t cmd gen. by $VER"
echo "\t cut drop => $CUTDUE sec."
echo "\t dueration=> $DUE sec."
#=========================================================== action DONE
#exit  0

#
#  refer:
#
# How To Format Date and Time in Linux, macOS, and Bash?
#  https://www.shell-tips.com/linux/how-to-format-date-and-time-in-linux-macos-and-bash/
# bash - Convert seconds to hours, minutes, seconds - Stack Overflow
#  https://stackoverflow.com/questions/12199631/convert-seconds-to-hours-minutes-seconds
# linux - Bash: calculate the time elapsed between two timestamps - Unix & Linux Stack Exchange
#  https://unix.stackexchange.com/questions/387010/bash-calculate-the-time-elapsed-between-two-timestamps
# linux - Bash script: difference in minutes between two times - Stack Overflow
#  https://stackoverflow.com/questions/14309032/bash-script-difference-in-minutes-between-two-times
# ...
