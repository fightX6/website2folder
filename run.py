#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
# Created by xf on 2017/7/4.
from config import Config
from parser_html import ParserHtml
import threadpool
import os


def filecreate(path, content):
    filepath = os.path.split(path)[0]
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    f = open(path, "w")
    f.write(content)
    f.flush()
    f.close()


def parser(html):
    content = html['file']['content']
    path = html['file']['path']
    print(path)
    for kurl, vurl in html['url_mapping'].items():
        content = content.replace(kurl, vurl)
    for kurl, vurl in html['children_url_mapping'].items():
        content = content.replace(kurl, vurl)
    filecreate(path['abspath'], content)


def run():
    root = ParserHtml(u'http://www.iconfont.cn/')
    root.parser()
    requests = threadpool.makeRequests(parser, Config.files)
    [Config.pool.putRequest(req) for req in requests]
    Config.pool.wait()

if __name__ == "__main__":
    run()
