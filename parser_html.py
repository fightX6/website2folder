#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
# Created by xf on 2017/7/4.
from config import Config
from parser import Parser
# 解析html
from bs4 import BeautifulSoup

__all__ = ['ParserHtml']


class ParserHtml(Parser):

    def __init__(self, wait_parse_url, parent_file=None):
        super().__init__(wait_parse_url, parent_file)

    def parser(self):
        """
        读取文件转换文件内容
        :return: 
        """
        super().parser()
        Config.files.append(self.current_file)
        file = self.current_file[u'file'].content
        # 自己的映射
        self.current_file[u'url_mapping'][self.url] = self.current_file[u'file'][u'path'][u'path']

        soup = BeautifulSoup(file)
        # 解析head里的 link 和 script
        for tag in soup.head.descendants:
            print(u'head的所有子孙标签', tag)
            url = self.parser_attrs(tag)
            p = ParserHtml(url, self.current_file)
            self.current_file[u'children_url_mapping'][url] = p.current_file[u'file'][u'path'][u'path']
            # Config.files_mapping[url] = p.current_file[u'file'][u'path'][u'path']
        # 解析body里的 a 、 img 、script
        for tag in soup.body.descendants:
            print(u'body的所有子孙标签', tag)
            url = self.parser_attrs(tag)
            Config.files_mapping[url] = ''
            p = ParserHtml(url, self.current_file)
            self.current_file[u'children_url_mapping'][url] = p.current_file[u'file'][u'path'][u'path']
            # Config.files_mapping[url] = p.current_file[u'file'][u'path'][u'path']

    @staticmethod
    def parser_attrs(tag):
        url = ''
        attrs = tag.attrs
        if tag.name == 'link':
            url = attrs['href']
        if tag.name == 'script':
            url = attrs['src']
        if tag.name == 'a':
            url = attrs['href']
        if tag.name == 'img':
            url = attrs['href']
        return url

