"""Auto converter encodings to utf8
#tags utility,py4zh
It will test utf8,gbk,big5,jp,kr to converter

发件人: HuangJiahua <jhuangjiahua@gmail.com>	
邮送域: googlegroups.com
回复: python-cn@googlegroups.com
收件人: "python.cn" <python-cn@googlegroups.com>
日期: 2006-1-16 上午12:11
主题: Re: 请问怎样得到一个文件的编码？
http://groups.google.com/group/python-cn/browse_frm/thread/3544d5a05783dc96

"""

#!/usr/bin/python
# coding:UTF-8
# Author: Huang Jiahua <jhuangjiahua@gmail.com>
#测试的编码类型
encc=''
def zh2utf8(stri):
       """Auto converter encodings to utf8

       It will test utf8,gbk,big5,jp,kr to converter"""
       global encc
       for c in ('utf-8', 'gbk', 'big5', 'jp',
'euc_kr','utf16','utf32'):
               encc = c
               try:
                       return stri.decode(c).encode('utf8')
               except:
                       pass
       encc = 'unk'
       return stri

if __name__=="__main__":
       # 命令行测试
       import sys
##      sys.setappdefaultencoding('unicode')
       if len(sys.argv) > 1:
               stri = sys.argv[1]
       else:
               stri = sys.stdin.read()
       print zh2utf8(stri)
       print 'encc:',encc