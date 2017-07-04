#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import mimetypes
from urllib.request import *
import os
import threadpool
import configparser
import codecs


__all__ = ['Config']

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
        contenttype = remote_file.getheaders(u'Content-Type')[0].split(u';')[0].strip()  # text/html; charset=utf-8
        for k, v in mimetypes.types_map.items():
            if v.lower() == contenttype.lower():
                return k
        return '.txt'

    @staticmethod
    def encode(remote_file):
        """
        :param remote_file: 远程url的类文件对象
        :return: 文件编码 默认 utf-8
        """
        header_contenttype = remote_file.getheaders(u'Content-Type')[0].strip()  # text/html; charset=utf-8
        # contenttype = header_contenttype.split(';')[0].strip()  # text/html
        encoder = u'utf-8'
        if str.find(u'html'):
            encoder = header_contenttype.split(u';')[1].split(u'=')[1].strip()
        return encoder

    @staticmethod
    def path(path, ext):
        """
        :param path: 获取的网络路径
        :param ext:  后缀带 . 
        :return: { 'abspath':'','path':''}
        """
        if path == u'':
            path = u'index'
        basepath = getconfig(u'path', u'basepath', u'F:\\work_python\\website2folder\\web\\')
        otherdir = getconfig(u'path', u'otherdir', u'/other/')
        jsdir = getconfig(u'path', u'jsdir', u'/js/')
        cssdir = getconfig(u'path', u'cssdir', u'/css/')
        imgdir = getconfig(u'path', u'imgdir', u'/images/')
        htmldir = getconfig(u'path', u'htmldir', u'/')
        # basepath = u'F:\\work_python\\website2folder\\web\\'
        # otherdir = u'/other/'
        # jsdir = u'/js/'
        # cssdir = u'/css/'
        # imgdir = u'/images/'
        # htmldir = u'/'
        ext = ext.lower()
        if str.index(u'.') == -1:
            path = path + ext
        if ext == u'.js':
            return {
                u'abspath': os.path.abspath(basepath + jsdir + path),
                u'path': pathname2url(jsdir + path),
                u'ext': ext
            }
        elif ext == u'.css':
            return {
                u'abspath': os.path.abspath(basepath + cssdir + path),
                u'path': pathname2url(cssdir + path),
                u'ext': ext
            }
        elif ext == u'.jpg' or ext == u'.jpeg' or ext == u'.png' or ext == u'.gif' or ext == u'.bmp':
            return {
                u'abspath': os.path.abspath(basepath + imgdir + path),
                u'path': pathname2url(imgdir + path),
                u'ext': ext
            }
        elif ext == u'html':
            return {
                u'abspath': os.path.abspath(basepath + htmldir + path),
                u'path': pathname2url(htmldir + path),
                u'ext': ext
            }
        else:
            return {
                u'abspath': os.path.abspath(basepath + otherdir + path),
                u'path': pathname2url(otherdir + path),
                u'ext': ext
            }

