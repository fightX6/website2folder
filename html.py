#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import re  # 正则模块

__all__ = ['Html']


class Html:
    def __init__(self, basedir):
        """
        :param basedir: 用来存放提取的html的文件夹根路径
        """
        self.basedir = self.__formatter(basedir)
        self.otherdir = '/other/'
        self.jsdir = '/js/'
        self.cssdir = '/css/'
        self.imgdir = '/images/'
        self.htmldir = '/'
        self.re_js = re.compile(r'<script.*?href=.*?(<\/script>|\/>)', re.I)
        self.re_css = re.compile(r'<link.*?href=.*?(<\/link>|\/>)', re.I)

    @staticmethod
    def __formatter(path):
        """
        :param path: 需要格式化的路径 
        :return: 返回结束不带/的路径 
        """
        path = path.replace('\\', '/')
        if path.endswith('/'):
            path = path[:len(path) - 1]
        return path


if __name__ == "__main__":
    pass