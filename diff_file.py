# -*- coding: utf-8 -*-
#对比2个文件的差异，并生成html页面展示

import difflib
hd = difflib.HtmlDiff()

mems = loads = ''

with open('/etc/passwd','r') as f:
    loads = f.readlines()

with open('/tmp/passwd', 'r') as f:
    mems = f.readlines()

with open('diff.html','a+') as f:
    f.write(hd.make_file(loads,mems))
