#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
# Created by xf on 2017/7/4.
from config import Config
import urllib
# from parser import Parser
# 解析html
import bs4
from bs4 import BeautifulSoup
import gzip
from io import StringIO

__all__ = ['ParserHtml']


class ParserHtml:

    def __init__(self, wait_parse_url, parent_file=None):
        # super().__init__(wait_parse_url, parent_file)
        self.url = wait_parse_url
        self.current_file = {
            u"url": wait_parse_url,
            u"file": {
                u'content': None,
                u'path': None
            },
            u"parent_file": parent_file,
            # 真实url 映射 转换后的url
            u'url_mapping': {},
            # 真实url 映射 转换后的url
            u"children_url_mapping": {}
        }

    def parser(self):
        """
        读取文件转换文件内容
        :return: 
        """
        self.readfile()
        Config.files.append(self.current_file)
        file = self.current_file[u'file'][u'content']
        ext = self.current_file[u'file'][u'path'][u'ext']
        # 自己的映射
        self.current_file[u'url_mapping'][self.url] = self.current_file[u'file'][u'path'][u'path']
        if ext == '.html':
            soup = BeautifulSoup(file, u"html.parser")
            # 解析head里的 link 和 script
            for tag in soup.head.contents:
                if type(tag) == bs4.element.NavigableString:
                    continue
                # print(u'head的所有子孙标签', tag)
                url = self.parser_attrs(tag)
                if url is None or url == '':
                    continue
                p = ParserHtml(url, self.current_file)
                p.parser()
                self.current_file[u'children_url_mapping'][url] = p.current_file[u'file'][u'path'][u'path']
                # Config.files_mapping[url] = p.current_file[u'file'][u'path'][u'path']
            # 解析body里的 a 、 img 、script
            for tag in soup.body.descendants:
                if type(tag) == bs4.element.NavigableString:
                    continue
                # print(u'body的所有子孙标签', tag)
                url = self.parser_attrs(tag)
                if url is None or url == u'':
                    continue
                Config.files_mapping[url] = ''
                p = ParserHtml(url, self.current_file)
                p.parser()
                self.current_file[u'children_url_mapping'][url] = p.current_file[u'file'][u'path'][u'path']
                # Config.files_mapping[url] = p.current_file[u'file'][u'path'][u'path']

    def readfile(self):
        # 准备参数
        url = self.url
        file = self.current_file[u'file']
        if self.current_file[u'parent_file'] is not None:
            parent_url = self.current_file[u'parent_file']['url']
        else:
            parent_url = url

        if url.startswith(u'//'):  # href="//libs.baidu.com"
            scheme = u'http'
            if parent_url.startswith(u'https:'):
                scheme = parent_url[0:5]
            url = scheme + ':' + url
        if url.startswith(u'data'):  # data:image/png;base64,iVBORw.....
            # url 可能是data:image/png;这种类型的图片 不做解析
            return
        if not url.startswith(u'http'):  # ../  及  /...
            url = urllib.parse.urljoin(parent_url, url)  # 从相对路径获取绝对路径

        # 开始解析
        # urlparse返回 ParseResult(scheme='http', netloc='segmentfault.com',
        # path='/blog/biu/1190000000330941', params='', query='', fragment='')
        result = urllib.parse.urlparse(url)
        f = urllib.request.urlopen(url)  # 创建一个表示远程url的类文件对象，然后像本地文件一样操作这个类文件对象来获取远程数据
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

        isGzip = f.info().get(u'Content-Encoding')
        if isGzip == 'gzip':
            compresseddata = f.read()
            compressedstream = StringIO.StringIO(compresseddata)
            gzipper = gzip.GzipFile(fileobj=compressedstream)
            data = gzipper.read()
        else:
            data = f.read()
        data = data.decode(Config.encode(f.info()))
        file[u'content'] = data
        f.close()
        file[u'path'] = Config.path(result.path, Config.ext(f.info()))  # 从根路径开始的路径

    # def handlebinarydata(self, strdata):
    #     content_type = strdata.split(';')[0].split(':')[1]
    #     data = base64.b64decode(strdata)
    #     with open('', 'wb') as f:
    #         f.write(data)
    #         f.close()

    @staticmethod
    def parser_attrs(tag):
        attrs = tag.attrs
        try:
            if tag.name == 'link':
                return attrs['href']
            if tag.name == 'script':
                return attrs['src']
            if tag.name == 'a':
                return attrs['href']
            if tag.name == 'img':
                return attrs['href']
        except Exception as ex:
            print(ex)
        return None

