#!/usr/local/bin/python
#tags utility,Subversion,hooks
#coding=utf-8
"""
SVN 事务日志处理
    - 使用固定的参数来自动响应检入后续操作:
        - 记录检入活动信息到每日log文件
"""
##  Zoomq::060110 fixed log exp. esp. for woodpecker repo.
## only record commit-log of woodpecker


import sys,os,time

CHMOD = "/bin/chmod"
CHOWN = "/usr/sbin/chown"
LOOK = "/usr/local/bin/svnlook"
SVN = "/usr/local/bin/svn"
log="/var/log/svn/woodpecker-ci.log"
daylog = "%s-%s.log"%(log[:-4]
                    ,time.strftime("%y%m%d",
                                    time.localtime()))
LOGFILE = daylog
f = open( LOGFILE, "a+" )
TSTAMP = "%s"%time.strftime("%y-%m-%d %H:%M:%S", time.localtime())

### hook matter
MARK = "woodpecker"
MOD = "woodpecker"
AIM = "/path/to/woodpecker/repos/"
def autoco(dirs,svn,mark,aim,mod):
    """auto co all matter files:
        - svn SVNLOOK where
        - mark the mark of matter
        - aim where want to co
        - mod 指定的模块
    """
    print >> f,dirs
    if mark in dirs:
        print >> f,TSTAMP+" marked::OK! up::"+aim+mod
        upsvn = svn+" update %s"%(aim+mod)
        print >> f,TSTAMP+upsvn
        up = os.popen(upsvn).read().strip()
        print >> f,up
    else:
        print >> f,TSTAMP+" marked::NO! up::nothing"
def changedirs(look,rev,repos):
    """list all changed dir
    """
    dirs = os.popen( look+" changed -r "+ rev + " " + repos).read().strip()
    return dirs
def chkdirmod(cmod,cown,path,umark):
    """chmod and chown the aim path
    """
    exp = os.popen(cmod+" -R "+umark+" "+path).read().strip()
    exp += os.popen(cown+" -R www:www "+path).read().strip()    
    return exp
def logcommit(look,rev,repos):
    """log commit info...
    """
    log = os.popen( look+" author -r "+ rev + " "+ repos).read().strip()
    print >> f," "*4+"%s commited;%s"%(str(log),repos)
    #return log..
    
def usage():
    print "Usage: " + sys.argv[0] + " REPOS REV\n"
    print >> f,TSTAMP+"Usage: " + sys.argv[0] + " REPOS REV"
    sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
    # start hook matter...
    repos = sys.argv[1]
    rev = sys.argv[2]        
    print >> f,TSTAMP+" >>>>>> woodpecker up rev::"+rev
    print >> f,changedirs(LOOK,rev,repos)
    logcommit(LOOK,rev,repos)
    
    print >> f,TSTAMP+" <<<<<< woodpecker repo commit DONE! "
    