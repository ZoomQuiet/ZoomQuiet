# crontab - zoomq's crontab for Zues
#
SHELL=/bin/sh
PATH=/home/zoomq/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
#HOME=/home/zoomq/zoomquiet.org
MAILTO=Zoom.Quiet@gmail.com
#
#minute	hour	mday	month	wday	command
###zoomq:091129 paaended for obp.zoomquiet auto build Sphinx+.dot
*/15   *   *   *   * /home/zoomq/zoomquiet.org/_cron/obp-shpinx-up.sh
*   */8   *   *   * /home/zoomq/zoomquiet.org/_cron/obp-idx-up.sh


