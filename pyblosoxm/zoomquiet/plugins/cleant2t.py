# -*- coding: utf-8 -*-
# =============================================================
# 快速预处理 t2t 生成的html :
#   - 清除 <body/> 之外的代码
#   - 将 title 单独放在头部,以便 PyBlosxom 识别使用
# =============================================================
__version__ = 'cleant2t.py v10.4.13'
__author__ = 'Zoom.Quiet <zoomq at zeuux dot org>'

import sys

def clean2entry(htmf):
    html = open(htmf).readlines()
    #print html[9:-1]
    #print html[5][7:-9]
    body = "".join(html[9:-1])
    #return "%s\n%s"%(html[5][7:-9],body)
    open("%s.txt"%htmf,"w").write("%s\n%s"%(html[5][7:-9],body))
    print "cleaned,ans exp. as %s.txt"%htmf

if __name__ == '__main__':      # this way the module can be
    if 2 != len(sys.argv):
        print """ %s usage::
$ python cleant2t.py path/2/t2t/export/entry.html
        """ % VERSION
    else:
        htmfile = sys.argv[1]
        clean2entry(htmfile)

