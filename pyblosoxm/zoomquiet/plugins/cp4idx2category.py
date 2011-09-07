# -*- coding: utf-8 -*-
'''
将 category_static.py 生成的树状分类索引页面，复制并修订为各个目录中的 index.html
'''
__version__ = 'cp4idx2category v11.09.7'
__author__ = 'Zoom.Quiet <zoomquiet+pyb at gmail dot com>'

import os
import sys
import re
import shutil


def cp4gen(path):
    #print path
    IDX = "%s/category-index.html"% path
    p = re.compile("%s\/\d{4}"%path )
    for root, dirs, files in os.walk(path):
        if path == root:
            pass
        elif p.match(root):
            pass
        elif "plugin_info" in root:
            pass
        else:
            #print root.replace(path,"")  #,dirs,files
            aimpath = root.replace(path,"")
            exp = ""
            for i in open(IDX,'r'):
                if '<span id="' in i:
                    if aimpath in i:
                        exp += i
                else:
                    exp += i

            open("%s/index.html"% root,"w").write(exp)
    return

if __name__ == '__main__':      # this way the module can be
    if 2 != len(sys.argv):
        print """ %s usage::
$ python cp4idx2category.py path/2/_static
            |               +- 生成的静态页面入口
            +- 脚本自身
        """ % VERSION
    else:
        path = sys.argv[1]
        cp4gen(path)

