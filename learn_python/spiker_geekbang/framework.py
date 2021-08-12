# -*- coding: UTF-8 -*-

import pycurl

from io import StringIO

c = pycurl.Curl()

c.setopt(pycurl.URL, "https://time.geekbang.org/column/article/6463")

b = StringIO.StringIO()

c.setopt(pycurl.WRITEFUNCTION, b.write)

c.setopt(pycurl.FOLLOWLOCATION, 1)

c.setopt(pycurl.MAXREDIRS, 5)

c.perform()

html = b.getvalue()

# print html

fh = open("file.html", "w")

fh.write(html)

fh.close()
