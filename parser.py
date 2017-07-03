#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import os
import base64
import uuid
import mimetypes
# 请求url, 支持 HTTP(0.9/1.0) / FTP / 本地文件 / URL
from urllib.request import *
# 解析url, 支持 file / ftp / gopher / hdl / http / https / imap / mailto / mms / news / nntp /
# prospero / rsync / rtsp / rtspu / sftp / shttp / sip / sips / snews / svn / svn+ssh / telnet / wais
from urllib.parse import *
# 解析html
# from bs4 import BeautifulSoup


class Parser:
    def __init__(self, html, url):
        """
        :param html: 全局对象
        :param url: 要爬取的网站地址 
        """
        self.url = url
        self.domain = url
        self.html = html
        self.files = []
        self.readfile(self.url)
        mimetypes.init(['mimetypes.txt'])

    def readfile(self, url):
        # TODO url 可能是data:image/png;这种类型的图片
        if not url.startswith('http') and not url.startswith('data'):
            url = urljoin(self.domain, url)  # 从相对路径获取绝对路径
        # urlparse返回 ParseResult(scheme='http', netloc='segmentfault.com',
        # path='/blog/biu/1190000000330941', params='', query='', fragment='')
        result = urlparse(url)

        file = {}

        f = urlopen(url)  # 创建一个表示远程url的类文件对象，然后像本地文件一样操作这个类文件对象来获取远程数据
        # file.info = f.info()  # http header:返回一个httplib.HTTPMessage 对象,表示远程服务器返回的头信息
        # file.code = f.getcode()  # 返回Http状态码。如果是http请求，200表示请求成功完成;404表示网址未找到
        # file.requestURL = f.geturl()  # 返回请求的url
        # for line in f.readlines():  # 就像在操作本地文件
        """
            调用read()会一次性读取文件的全部内容，如果文件有10G，内存就爆了，所以，要保险起见，
            可以反复调用read(size)方法，每次最多读取size个字节的内容。另外，调用readline()可以每次读取一行内容，
            调用readlines()一次读取所有内容并按行返回list。
        """
        #   pass
        file.content = f.read().decode("utf-8")

        content_type = f.getheaders('Content-Type')[0].split(';')[1]
        f.close()
        self.files.append(file)

    def handlebinarydata(self, strdata):
        content_type = strdata.split(';')[0].split(':')[1]

        data = base64.b64decode(strdata)
        with open('', 'wb') as f:
            f.write(data)
            f.close()

    @staticmethod
    def getext(content_type):
        for k, v in mimetypes.types_map.items():
            if v.lower() == content_type.lower():
                return k
        return '.txt'

if __name__ == "__main__":
    print('/blog/biu/1190000000330941'.split('/')[-1])
    mimetypes.init(['mimetypes.txt'])
    for k, v in mimetypes.types_map.items():
        if v.lower() == 'image/jpeg'.lower():
            print(k, v)
    pass



