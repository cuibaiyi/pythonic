# -*- coding: utf-8 -*-
```
对比2个文件的差异，并生成html页面展示
```
import difflib
hd = difflib.HtmlDiff()

mems = loads = ''

with open('/etc/passwd','r') as load:
    loads = load.readlines()

with open('/tmp/passwd', 'r') as mem:
    mems = mem.readlines()

with open('diff.html','a+') as fo:
    fo.write(hd.make_file(loads,mems))
