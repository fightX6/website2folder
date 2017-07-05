#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import mimetypes
from urllib.request import pathname2url
import os
import threadpool
import configparser
import codecs
import sys
import logging
from logging import config
import uuid

config.fileConfig("resources/log.conf")
console = logging.getLogger("simpleExample")

__all__ = ['Config']

for path in sys.path:
    console.debug('sys.path:' + path)

# 读取配置文件得到配置文件对象
cp = configparser.ConfigParser()
with codecs.open(u'resources/conf.conf', 'r', encoding='utf-8') as f:
    cp.read_file(f)


def getconfig(setion, option, default=None):
    """
    获取配置文件的值
    :param setion: 
    :param option: 
    :param default: 
    :return: 
    """
    val = cp.get(setion, option)
    if default is not None and val is None:
        val = default
    print(setion, '----', option, '---', val)
    return val

# 定义线程池
# 从配置文件获取配置
pool = threadpool.ThreadPool(int(getconfig(u'threadpool', u'num', 5)))

basepath = getconfig(u'path', u'basepath', u'F:\\work_python\\website2folder\\web\\')
otherdir = getconfig(u'path', u'otherdir', u'/other/')
jsdir = getconfig(u'path', u'jsdir', u'/js/')
cssdir = getconfig(u'path', u'cssdir', u'/css/')
imgdir = getconfig(u'path', u'imgdir', u'/images/')
htmldir = getconfig(u'path', u'htmldir', u'/')

# 初始化后缀对应流类型文件
mimetypes.init([u'mimetypes.txt'])


class Config:
    # 定义线程池
    pool = pool
    # 真实url 映射 转换后的url
    files_mapping = {}
    # 所有文件
    files = []

    def __init__(self):
        pass

    @staticmethod
    def ext(remote_file):
        """
        :param remote_file: 远程url的类文件对象
        :return: ext 文件后缀带 . 的
        """
        contenttype = remote_file.get(u'Content-Type').split(u';')[0].strip()  # text/html; charset=utf-8
        for k, v in mimetypes.types_map.items():
            if v.lower() == contenttype.lower():
                if k == '.htm':
                    k = '.html'
                return k
        return '.txt'

    @staticmethod
    def encode(remote_file):
        """
        :param remote_file: 远程url的类文件对象
        :return: 文件编码 默认 utf-8
        """
        print(remote_file.get('Content-Type'))
        header_contenttype = remote_file.get(u'Content-Type').strip().lower()  # text/html; charset=utf-8
        # contenttype = header_contenttype.split(';')[0].strip()  # text/html
        encoder = u'utf-8'
        if header_contenttype.find(u'charset') == -1:
            return encoder
        if header_contenttype.find(u'html'):
            encoder = header_contenttype.split(u';')[1].split(u'=')[1].strip()
        return encoder

    @staticmethod
    def path(srcpath, ext):
        """
        :param srcpath: 获取的网络路径
        :param ext:  后缀带 . 
        :return: { 'abspath':'','path':''}
        """
        filepath = srcpath
        if filepath == u'' or filepath == u'/':
            filepath = u'index'
        ext = ext.lower()
        if filepath.find(u'.') == -1:
            filepath = filepath + ext
        if ext == u'.js':
            return {
                u'abspath': os.path.abspath(basepath + jsdir + filepath),
                u'path': pathname2url(jsdir + filepath).replace('//', '/'),
                u'ext': ext
            }
        elif ext == u'.css':
            return {
                u'abspath': os.path.abspath(basepath + cssdir + filepath),
                u'path': pathname2url(cssdir + filepath).replace('//', '/'),
                u'ext': ext
            }
        elif ext == u'.jpg' or ext == u'.jpeg' or ext == u'.png' or ext == u'.gif' or ext == u'.bmp':
            return {
                u'abspath': os.path.abspath(basepath + imgdir + filepath),
                u'path': pathname2url(imgdir + filepath).replace('//', '/'),
                u'ext': ext
            }
        elif ext == u'.html':
            return {
                u'abspath': os.path.abspath(basepath + htmldir + filepath),
                u'path': pathname2url(htmldir + filepath).replace('//', '/'),
                u'ext': ext
            }
        else:
            return {
                u'abspath': os.path.abspath(basepath + otherdir + filepath),
                u'path': pathname2url(otherdir + filepath).replace('//', '/'),
                u'ext': ext
            }

