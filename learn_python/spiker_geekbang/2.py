# -*- coding: UTF-8 -*-

import urllib.request

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def getHtml(url):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    html = response.read()
    return html


def saveHtml(file_name, file_content):
    with open(file_name.replace('/', '_') + '.html', 'wb') as f:
        f.write(file_content)


filePath = "/Users/knight/Desktop/mobvoi/极客/从0开始学架构/架构设计的历史背景.html"

html = getHtml("https://time.geekbang.org/column/article/6463")
saveHtml(filePath, html)
print("结束")
