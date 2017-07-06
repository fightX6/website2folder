#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
# Created by xf on 2017/7/4.
from config import Config
from parser_html import ParserHtml
import threadpool
import os


def filecreate(path, content, encode):
    filepath = os.path.split(path)[0]
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    if type(content) == str:
        f = open(path, "w", encoding=encode)
        f.write(content)
        f.flush()
        f.close()
    if type(content) == bytes:
        f = open(path, "wb")
        f.write(content)
        f.flush()
        f.close()


def parser(html):
    content = html['file']['content']
    encode = html['file']['encode']
    print(type(content))
    path = html['file']['path']
    print(path)
    text = content
    for kurl, vurl in html['url_mapping'].items():
        if type(text) == str:
            text = text.replace(kurl, vurl)
    filecreate(path['abspath'], text, encode)


def run():
    root = ParserHtml(u'http://www.iconfont.cn/')
    root.parser()
    # requests = threadpool.makeRequests(parser, Config.files)
    # [Config.pool.putRequest(req) for req in requests]
    # Config.pool.wait()
    for file in Config.files:
        parser(file)

if __name__ == "__main__":
    run()
